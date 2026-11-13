"""PDD ilustrativa: nao representa a politica contabil real da Vitru."""
from datetime import date
from decimal import Decimal
from collections import defaultdict
from .io_utils import read_csv,write_csv,write_json,cents,br,digest,add_manifest

BANDS=('A_VENCER','1_30','31_60','61_90','91_120','121_MAIS')
def band(due,asof):
    days=(date.fromisoformat(asof)-date.fromisoformat(due)).days
    if days<=0:return BANDS[0]
    if days<=30:return BANDS[1]
    if days<=60:return BANDS[2]
    if days<=90:return BANDS[3]
    if days<=120:return BANDS[4]
    return BANDS[5]
def load_curves(file):
    required=('MARCA','MODALIDADE','FAIXA','TAXA','VERSAO')
    records=read_csv(file,required)
    out={};versions=set()
    for r in records:
        key=(r['MARCA'],r['MODALIDADE'],r['FAIXA'])
        if key in out:raise ValueError('Curva duplicada: '+str(key))
        rate=Decimal(r['TAXA'].replace(',','.'))
        if rate<0 or rate>1 or r['FAIXA'] not in BANDS:raise ValueError('Taxa/faixa invalida')
        versions.add(r['VERSAO']);out[key]=rate
    if len(versions)!=1:raise ValueError('A demo usa uma unica versao de curva por execucao')
    return out,versions.pop()
def evaluate(portfolio,curves,asof):
    out=[];seen=set()
    for r in portfolio:
        title=r['TITULO_ID']
        if not title or title in seen:raise ValueError('Titulo vazio/duplicado')
        seen.add(title)
        balance=cents(r['SALDO_ABERTO'])
        if balance<0:raise ValueError('Saldo negativo: '+title)
        bucket=band(r['VENCIMENTO'],asof)
        key=(r['MARCA'],r['MODALIDADE'],bucket)
        if key not in curves:raise ValueError('Falta curva para '+str(key))
        rate=curves[key]
        pdd=int((Decimal(balance)*rate).quantize(Decimal('1')))
        out.append(dict(TITULO_ID=title,MARCA=r['MARCA'],MODALIDADE=r['MODALIDADE'],FAIXA=bucket,SALDO_ABERTO=br(balance),TAXA=str(rate),PDD_ILUSTRATIVA=br(pdd)))
    return out
def control(summary,control_file):
    controls=read_csv(control_file,('MARCA','TOTAL_ESPERADO'))
    bybrand=defaultdict(int)
    for r in summary:bybrand[r['MARCA']]+=cents(r['SALDO_ABERTO'])
    results=[]
    for r in controls:
        actual=bybrand.pop(r['MARCA'],0);target=cents(r['TOTAL_ESPERADO'])
        results.append({'MARCA':r['MARCA'],'ESPERADO':br(target),'CALCULADO':br(actual),'DELTA':br(actual-target),'STATUS':'OK' if actual==target else 'DIVERGENTE'})
    for brand,value in bybrand.items():results.append({'MARCA':brand,'ESPERADO':'N/A','CALCULADO':br(value),'DELTA':'N/A','STATUS':'SEM_CONTROLE'})
    return results
def paliativa(portfolio_file,curves_file,control_file,output,asof='2026-09-30'):
    portfolio=read_csv(portfolio_file,('TITULO_ID','MARCA','MODALIDADE','VENCIMENTO','SALDO_ABERTO'))
    curves,version=load_curves(curves_file)
    result=evaluate(portfolio,curves,asof)
    recon=control(result,control_file)
    from pathlib import Path
    output=Path(output)
    add_manifest(output/'manifest_entrada.json',portfolio_file,asof+'|carteira')
    add_manifest(output/'manifest_entrada.json',curves_file,asof+'|curva')
    add_manifest(output/'manifest_entrada.json',control_file,asof+'|controle')
    write_csv(output/'gold_pdd_ilustrativa.csv',result,('TITULO_ID','MARCA','MODALIDADE','FAIXA','SALDO_ABERTO','TAXA','PDD_ILUSTRATIVA'))
    write_csv(output/'reconciliacao.csv',recon,('MARCA','ESPERADO','CALCULADO','DELTA','STATUS'))
    total=sum(cents(x['PDD_ILUSTRATIVA']) for x in result)
    status='APROVADA_DEMO' if all(x['STATUS']=='OK' for x in recon) else 'BLOQUEADA'
    report={'modo':'paliativa','ref':asof,'curva_versao':version,'titulos':len(result),'pdd_ilustrativa':br(total),'validacao_controle':status,'aviso':'Taxas e regras sao ficticias; nunca contabilizar'}
    write_json(output/'resumo.json',report)
    return report

def portfolio_from_events(events,position_date,knowledge_date):
    required=('TITULO_ID','EVENTO_ID','EFETIVO_EM','CONHECIDO_EM','TIPO','DELTA','MARCA','MODALIDADE','VENCIMENTO')
    seen=set();bytitle={};allowed={'EMISSAO','PAGAMENTO','ESTORNO','AJUSTE'}
    for event in events:
        for field in required:
            if field not in event:raise ValueError('Evento sem campo: '+field)
        ev_id=event['EVENTO_ID']
        if not ev_id or ev_id in seen:raise ValueError('Evento duplicado/sem id')
        seen.add(ev_id)
        if event['TIPO'] not in allowed:raise ValueError('Evento desconhecido')
        if event['EFETIVO_EM']>position_date or event['CONHECIDO_EM']>knowledge_date:continue
        t=event['TITULO_ID'];info=(event['MARCA'],event['MODALIDADE'],event['VENCIMENTO'])
        if t not in bytitle:bytitle[t]=[info,0]
        elif bytitle[t][0]!=info:raise ValueError('Metadados de titulo conflitantes')
        delta=cents(event['DELTA'])
        if event['TIPO']=='EMISSAO' and delta<=0:raise ValueError('Emissao deveria ser positiva')
        if event['TIPO']=='PAGAMENTO' and delta>=0:raise ValueError('Pagamento deveria reduzir saldo')
        bytitle[t][1]+=delta
    output=[]
    for t,(info,balance) in bytitle.items():
        if balance<0:raise ValueError('Saldo final negativo para '+t)
        output.append(dict(TITULO_ID=t,MARCA=info[0],MODALIDADE=info[1],VENCIMENTO=info[2],SALDO_ABERTO=br(balance)))
    return sorted(output,key=lambda r:r['TITULO_ID'])
def definitiva(event_file,curves_file,output,position_date='2026-09-30',first_known='2026-09-30',latest_known='2026-10-07'):
    events=read_csv(event_file,('TITULO_ID','EVENTO_ID','EFETIVO_EM','CONHECIDO_EM','TIPO','DELTA','MARCA','MODALIDADE','VENCIMENTO'))
    curves,version=load_curves(curves_file)
    early=evaluate(portfolio_from_events(events,position_date,first_known),curves,position_date)
    latest=evaluate(portfolio_from_events(events,position_date,latest_known),curves,position_date)
    from pathlib import Path
    output=Path(output)
    for source,tag in [(event_file,'eventos'),(curves_file,'curvas')]:add_manifest(output/'manifest_entrada.json',source,position_date+'|'+tag)
    fields=('TITULO_ID','MARCA','MODALIDADE','FAIXA','SALDO_ABERTO','TAXA','PDD_ILUSTRATIVA')
    write_csv(output/'gold_pdd_conhecida_no_fechamento.csv',early,fields)
    write_csv(output/'gold_pdd_reprocessada_retroativo.csv',latest,fields)
    p1=sum(cents(r['PDD_ILUSTRATIVA']) for r in early);p2=sum(cents(r['PDD_ILUSTRATIVA']) for r in latest)
    report={'modo':'definitiva','posicao_em':position_date,'conhecimento_original':first_known,'conhecimento_reprocessado':latest_known,'versao_curva':version,'pdd_original':br(p1),'pdd_reprocessada':br(p2),'impacto_retroativo':br(p2-p1),'status':'DEMONSTRACAO_NAO_HOMOLOGADA'}
    write_json(output/'resumo.json',report)
    return report
