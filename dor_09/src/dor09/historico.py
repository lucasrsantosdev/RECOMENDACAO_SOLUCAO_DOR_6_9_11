"""Controle paliativo de fotos e motor bitemporal definitivo demonstrativo."""
from pathlib import Path
from collections import defaultdict
from datetime import date
import json
from .io_utils import read_csv,write_csv,write_json,cents,br,digest,sha,add_manifest
FIELDS=('TITULO_ID','MARCA','COMPETENCIA','VENCIMENTO','SALDO_ABERTO','STATUS')
EVENT_FIELDS=('TITULO_ID','EVENTO_ID','EFETIVO_EM','CONHECIDO_EM','TIPO','DELTA','MARCA','VENCIMENTO','REFERENCIA_ID')

def validate_snapshot(rows):
    seen=set()
    for r in rows:
        k=r['TITULO_ID']
        if not k or k in seen:raise ValueError('Titulo duplicado/sem id')
        seen.add(k)
        if cents(r['SALDO_ABERTO'])<0:raise ValueError('Saldo negativo')
        date.fromisoformat(r['VENCIMENTO'])
    return len(rows)

def capture(input_file, capture_id, output):
    """Copia fonte sem conversao; rejeita mudanca na mesma captura e adulteracao da RAW."""
    input_file=Path(input_file);out=Path(output)
    rows=read_csv(input_file,FIELDS);validate_snapshot(rows)
    entry,created=add_manifest(out/'manifests.json',input_file,capture_id)
    rawfile=out/'raw'/(capture_id+'.csv')
    rawfile.parent.mkdir(parents=True,exist_ok=True)
    if rawfile.exists():
        if digest(rawfile)!=entry['sha256']:raise ValueError('RAW previamente armazenada foi alterada')
    else:
        rawfile.write_bytes(input_file.read_bytes())
    return {'captura':capture_id,'qtd':len(rows),'sha256':entry['sha256'],'nova':created}

def compare_files(file_a,file_b,out):
    before=read_csv(file_a,FIELDS);after=read_csv(file_b,FIELDS)
    validate_snapshot(before);validate_snapshot(after)
    d1={r['TITULO_ID']:r for r in before};d2={r['TITULO_ID']:r for r in after}
    rows=[];counts=defaultdict(int)
    for key in sorted(set(d1)|set(d2)):
        b=d1.get(key);a=d2.get(key)
        if not b:typ='NOVO'
        elif not a:typ='AUSENTE_NA_FOTO_NOVA_NAO_EXCLUSAO'
        elif b!=a:typ='ALTERADO'
        else:typ='INALTERADO'
        counts[typ]+=1
        # Não tratar ausência como exclusão física; exigir flag de extracao completa.
        rows.append({'TITULO_ID':key,'TIPO':typ,'SALDO_ANTERIOR':b['SALDO_ABERTO'] if b else '', 'SALDO_ATUAL':a['SALDO_ABERTO'] if a else '', 'DELTA':br(cents(a['SALDO_ABERTO'] if a else 0)-cents(b['SALDO_ABERTO'] if b else 0)),'OBS':'Ausencia nao prova delete' if not a else ''})
    out=Path(out)
    write_csv(out/'comparacao_fotos.csv',rows,('TITULO_ID','TIPO','SALDO_ANTERIOR','SALDO_ATUAL','DELTA','OBS'))
    result={'resumo':dict(counts),'saldo_anterior':br(sum(cents(r['SALDO_ABERTO']) for r in before)),'saldo_atual':br(sum(cents(r['SALDO_ABERTO']) for r in after)), 'aviso':'Diferenca nao indica erro de origem sem eventos de justificativa'}
    write_json(out/'resumo_comparacao.json',result)
    return result

def paliativa(older,newer,out):
    out=Path(out)
    a=capture(older,'CAPTURA-20260930',out)
    b=capture(newer,'CAPTURA-20261005',out)
    comp=compare_files(out/'raw'/'CAPTURA-20260930.csv',out/'raw'/'CAPTURA-20261005.csv',out)
    return {'capturas':[a,b], 'comparacao':comp}

def replay(events,position_date,knowledge_date):
    """As-of bitemporal: movimentos efetivos ate D e conhecidos ate K."""
    seen=set();state={};valid={'EMISSAO','PAGAMENTO','ESTORNO','AJUSTE','RENEGOCIACAO','CANCELAMENTO'}
    relevant=[]
    for e in events:
        for f in EVENT_FIELDS:
            if f not in e:raise ValueError('Evento sem '+f)
        if not e['EVENTO_ID'] or e['EVENTO_ID'] in seen:raise ValueError('EVENTO_ID duplicado')
        seen.add(e['EVENTO_ID'])
        if e['TIPO'] not in valid:raise ValueError('Tipo de evento nao suportado')
        date.fromisoformat(e['EFETIVO_EM']);date.fromisoformat(e['CONHECIDO_EM'])
        if e['EFETIVO_EM']<=position_date and e['CONHECIDO_EM']<=knowledge_date:relevant.append(e)
    relevant.sort(key=lambda e:(e['EFETIVO_EM'],e['CONHECIDO_EM'],e['EVENTO_ID']))
    for e in relevant:
        title=e['TITULO_ID'];delta=cents(e['DELTA'])
        if e['TIPO']=='EMISSAO':
            if delta<=0 or title in state:raise ValueError('Emissao invalida ou repetida')
            state[title]={'MARCA':e['MARCA'],'VENCIMENTO':e['VENCIMENTO'],'SALDO':delta,'EVENTOS':[e['EVENTO_ID']]}
            continue
        if title not in state:raise ValueError('Movimento orfao: '+title)
        if (state[title]['MARCA'],state[title]['VENCIMENTO'])!=(e['MARCA'],e['VENCIMENTO']):raise ValueError('Conflito na chave do titulo')
        if e['TIPO']=='PAGAMENTO' and delta>=0:raise ValueError('Pagamento sem efeito redutor')
        if e['TIPO']=='ESTORNO' and delta<=0:raise ValueError('Estorno sem efeito positivo')
        if e['TIPO']=='CANCELAMENTO' and delta>0:raise ValueError('Cancelamento positivo')
        state[title]['SALDO']+=delta
        if state[title]['SALDO']<0:raise ValueError('Saldo negativo ao aplicar eventos')
        state[title]['EVENTOS'].append(e['EVENTO_ID'])
    return [{'TITULO_ID':key,'MARCA':v['MARCA'],'VENCIMENTO':v['VENCIMENTO'],'SALDO':br(v['SALDO']), 'EVENTOS':'|'.join(v['EVENTOS'])} for key,v in sorted(state.items())]

def definitiva(event_file,out,asof='2026-09-30',first_known='2026-09-30',later_known='2026-10-05'):
    events=read_csv(event_file,EVENT_FIELDS)
    old=replay(events,asof,first_known);new=replay(events,asof,later_known)
    out=Path(out);add_manifest(out/'manifests.json',event_file,asof+'|eventos')
    fields=('TITULO_ID','MARCA','VENCIMENTO','SALDO','EVENTOS')
    write_csv(out/'gold_fechamento_original.csv',old,fields)
    write_csv(out/'gold_posicao_recalculada.csv',new,fields)
    changes=[];b={r['TITULO_ID']:r for r in old};a={r['TITULO_ID']:r for r in new}
    for k in sorted(set(a)|set(b)):
        before=cents(b[k]['SALDO']) if k in b else 0;after=cents(a[k]['SALDO']) if k in a else 0
        if before!=after:changes.append({'TITULO_ID':k,'SALDO_NO_FECHAMENTO':br(before),'SALDO_REPROCESSADO':br(after),'IMPACTO':br(after-before)})
    write_csv(out/'gold_retroativos.csv',changes,('TITULO_ID','SALDO_NO_FECHAMENTO','SALDO_REPROCESSADO','IMPACTO'))
    total_old=sum(cents(x['SALDO']) for x in old);total_new=sum(cents(x['SALDO']) for x in new)
    result={'modo':'definitiva','posicao':asof,'conhecimento_original':first_known,'conhecimento_novo':later_known,'saldo_original':br(total_old),'saldo_reprocessado':br(total_new),'delta':br(total_new-total_old),'titulos_impactados':len(changes),'status':'DEMO_NAO_HOMOLOGADA'}
    write_json(out/'resumo.json',result)
    return result
