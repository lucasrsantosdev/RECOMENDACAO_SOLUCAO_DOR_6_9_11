"""CREDIN: ingestao de boletos + conciliacao por dominios. FIES e produto distinto."""
import csv
from pathlib import Path
from collections import defaultdict
from decimal import Decimal
from datetime import date, datetime
from .io_utils import read_csv,write_csv,write_json,cents,br,add_manifest
BILL_FIELDS=('NOSSO_NUMERO','CODIGO_RA','PARCELA','VALOR_TITULO','VALOR_PAGO','VENCIMENTO','DATA_COMPETENCIA')
BILL_OUT=('CHAVE_TITULO','RA','PARCELA','COMPETENCIA','VENCIMENTO','VALOR_EMITIDO','VALOR_PAGO','SALDO_ILUSTRATIVO')
RECON_OUT=('RA','MODALIDADE','SALDO_BOLETOS','SALDO_AR_14','SALDO_ERP','AF_DIVIDA_GERADA','AF_BOLSA_CONCEDIDA','DELTA_BOLETOS_AR','DELTA_BOLETOS_ERP','STATUS','MOTIVOS')

def load_72666(file):
    """Aceita exportacao autorizada em UTF-8 ou CP1252. Nao emite nomes/codigos de aluno."""
    path=Path(file)
    for encoding in ('utf-8-sig','cp1252'):
        try:
            with path.open('r',encoding=encoding,newline='') as handle:
                reader=csv.DictReader(handle,delimiter=';')
                missing=set(BILL_FIELDS)-set(reader.fieldnames or [])
                if missing:raise ValueError('Cabecalho 72666 incompleto: '+','.join(sorted(missing)))
                return list(reader),encoding
        except UnicodeDecodeError:
            continue
    raise ValueError('Codificacao nao suportada')

def parse_due(text):
    text=text.strip()
    for fmt in ('%Y-%m-%d','%d/%m/%Y'):
        try:return datetime.strptime(text,fmt).date().isoformat()
        except ValueError:pass
    raise ValueError('Vencimento nao reconhecido')

def parse_competence(text):
    text=text.strip()
    if len(text)==6 and text.isdigit() and 1<=int(text[4:])<=12:return text
    try:return datetime.strptime(text,'%m/%Y').strftime('%Y%m')
    except ValueError:raise ValueError('Competencia invalida') from None

def normalize_bills(records):
    """Saldo nominal simplificado: titulo-pago, NAO saldo contábil oficial."""
    seen={};valid=[];errors=[]
    for i,r in enumerate(records,1):
        ra=r['CODIGO_RA'].strip();number=r['NOSSO_NUMERO'].strip();installment=r['PARCELA'].strip()
        key=(number,ra,installment)
        if not all(key):
            errors.append({'LINHA':i,'CODIGO':'CHAVE_INCOMPLETA'});continue
        try:
            emitted=cents(r['VALOR_TITULO']);paid=cents(r['VALOR_PAGO'] or '0')
            if emitted<0 or paid<0 or paid>emitted:raise ValueError('Valores fora de regra demonstrativa')
            due=parse_due(r['VENCIMENTO'])
            comp=parse_competence(r['DATA_COMPETENCIA'])
        except (ValueError,TypeError):
            errors.append({'LINHA':i,'CODIGO':'VALOR_OU_DATA_INVALIDA'});continue
        signature=(emitted,paid,due,comp)
        if key in seen:
            errors.append({'LINHA':i,'CODIGO':'DUPLICATA_IDENTICA' if seen[key]==signature else 'CONFLITO_DE_CHAVE'})
            continue
        seen[key]=signature
        valid.append({'CHAVE_TITULO':'|'.join(key),'RA':ra,'PARCELA':installment,'COMPETENCIA':comp,'VENCIMENTO':due,'VALOR_EMITIDO':br(emitted),'VALOR_PAGO':br(paid),'SALDO_ILUSTRATIVO':br(emitted-paid)})
    return valid,errors

def paliativa(bills_file,control_file,out,competencia='202609',batch_id=None):
    if len(competencia)!=6 or not competencia.isdigit() or not 1<=int(competencia[4:])<=12:raise ValueError('Competencia invalida')
    if batch_id is None:batch_id=competencia+'-72666'
    rows,encoding=load_72666(bills_file)
    all_normalized,errors=normalize_bills(rows)
    normalized=[r for r in all_normalized if r['COMPETENCIA']==competencia]
    bycompetence=defaultdict(int)
    for r in all_normalized:bycompetence[r['COMPETENCIA']]+=1
    controls=read_csv(control_file,('INDICADOR','VALOR_ESPERADO'))
    expected={r['INDICADOR']:cents(r['VALOR_ESPERADO']) for r in controls}
    actual={'EMITIDO':sum(cents(r['VALOR_EMITIDO']) for r in normalized),'PAGO':sum(cents(r['VALOR_PAGO']) for r in normalized),'SALDO_ILUSTRATIVO':sum(cents(r['SALDO_ILUSTRATIVO']) for r in normalized)}
    check=[{'INDICADOR':k,'ESPERADO':br(v),'CALCULADO':br(actual.get(k,0)),'DELTA':br(actual.get(k,0)-v),'STATUS':'OK' if actual.get(k)==v else 'DIVERGENTE'} for k,v in expected.items()]
    for k in actual:
        if k not in expected:check.append({'INDICADOR':k,'ESPERADO':'N/A','CALCULADO':br(actual[k]),'DELTA':'N/A','STATUS':'SEM_CONTROLE'})
    out=Path(out)
    add_manifest(out/'manifest_lotes.json',bills_file,batch_id+'|boletos')
    add_manifest(out/'manifest_lotes.json',control_file,batch_id+'|controle')
    write_csv(out/'silver_boletos.csv',normalized,BILL_OUT)
    write_csv(out/'auditoria_competencias.csv',[{'COMPETENCIA':k,'REGISTROS':v} for k,v in sorted(bycompetence.items())],('COMPETENCIA','REGISTROS'))
    write_csv(out/'quarentena.csv',errors,('LINHA','CODIGO'))
    write_csv(out/'controle.csv',check,('INDICADOR','ESPERADO','CALCULADO','DELTA','STATUS'))
    status='APROVADO_DEMO' if normalized and not errors and all(x['STATUS']=='OK' for x in check) else 'BLOQUEADO'
    report={'modo':'paliativa','lote':batch_id,'encoding_origem':encoding,'linhas_brutas':len(rows),'competencias_distintas':len(bycompetence),'competencia_selecionada':competencia,'titulos_validos':len(normalized),'excecoes':len(errors),'status':status,'observacao':'saldo=VALOR_TITULO-VALOR_PAGO e regra ilustrativa; sem descontos, multa, juros, renegociacoes ou repasse oficial'}
    write_json(out/'resumo.json',report)
    return report

def uniq_by_ra(records,key,required):
    out={}
    for r in records:
        k=r[key]
        if not k or k in out:raise ValueError('RA vazia/duplicada no dominio '+key)
        for f in required:
            if f not in r:raise ValueError('Coluna ausente: '+f)
        out[k]=r
    return out

def reconcile(bill_rows,ar_rows,af_rows,erp_rows,tolerance_cents=0):
    """Compara boletos e fontes; AF apenas exibido, nunca igualado a AR automaticamente."""
    ar=uniq_by_ra(ar_rows,'RA',('SALDO_AR','MODALIDADE'))
    af=uniq_by_ra(af_rows,'RA',('DIVIDA_GERADA','BOLSA_CONCEDIDA','MODALIDADE'))
    erp=uniq_by_ra(erp_rows,'RA',('SALDO_CONTABIL','MODALIDADE'))
    by_ra=defaultdict(int)
    for b in bill_rows:by_ra[b['RA']]+=cents(b['SALDO_ILUSTRATIVO'])
    result=[];counts=defaultdict(int)
    for ra in sorted(set(by_ra)|set(ar)|set(af)|set(erp)):
        a=ar.get(ra);f=af.get(ra);e=erp.get(ra);total=by_ra.get(ra)
        mods={x['MODALIDADE'] for x in (a,f,e) if x}
        reasons=[]
        if len(mods)>1:reasons.append('MODALIDADE_CONFLITANTE')
        if total is None:reasons.append('SEM_BOLETOS_72666')
        if a is None:reasons.append('SEM_AR_14')
        if e is None:reasons.append('SEM_ERP')
        if f is None:reasons.append('SEM_AF_14B')
        arval=cents(a['SALDO_AR']) if a else None
        erpval=cents(e['SALDO_CONTABIL']) if e else None
        if total is not None and arval is not None and abs(total-arval)>tolerance_cents:reasons.append('DELTA_BOLETOS_AR')
        if total is not None and erpval is not None and abs(total-erpval)>tolerance_cents:reasons.append('DELTA_BOLETOS_ERP')
        status='CONCILIADO' if not reasons else 'PENDENTE'
        counts[status]+=1
        result.append({'RA':ra,'MODALIDADE':next(iter(mods)) if len(mods)==1 else 'A_VALIDAR','SALDO_BOLETOS':br(total) if total is not None else '', 'SALDO_AR_14':br(arval) if arval is not None else '', 'SALDO_ERP':br(erpval) if erpval is not None else '', 'AF_DIVIDA_GERADA':f['DIVIDA_GERADA'] if f else '', 'AF_BOLSA_CONCEDIDA':f['BOLSA_CONCEDIDA'] if f else '', 'DELTA_BOLETOS_AR':br(total-arval) if total is not None and arval is not None else '', 'DELTA_BOLETOS_ERP':br(total-erpval) if total is not None and erpval is not None else '', 'STATUS':status,'MOTIVOS':'|'.join(reasons)})
    return result,dict(counts)

def definitiva(bills_file,ar_file,af_file,erp_file,out,competencia='202609'):
    bills,enc=load_72666(bills_file)
    normalized,errors=normalize_bills(bills)
    if errors:raise ValueError('Quarentena de boletos nao vazia; nao produzir Gold')
    normalized=[r for r in normalized if r['COMPETENCIA']==competencia]
    ar=read_csv(ar_file,('RA','MODALIDADE','SALDO_AR'))
    af=read_csv(af_file,('RA','MODALIDADE','BOLSA_CONCEDIDA','DIVIDA_GERADA'))
    erp=read_csv(erp_file,('RA','MODALIDADE','SALDO_CONTABIL'))
    recon,counts=reconcile(normalized,ar,af,erp)
    out=Path(out)
    for source,role in ((bills_file,'72666'),(ar_file,'14'),(af_file,'14B'),(erp_file,'ERP')):
        add_manifest(out/'manifest_fontes.json',source,competencia+'|'+role)
    write_csv(out/'silver_boletos_normalizados.csv',normalized,BILL_OUT)
    write_csv(out/'gold_conciliacao_credito.csv',recon,RECON_OUT)
    write_csv(out/'pendencias.csv',[r for r in recon if r['STATUS']=='PENDENTE'],RECON_OUT)
    status='LIBERADA_APENAS_DEMO' if counts.get('PENDENTE',0)==0 and recon else 'BLOQUEADA'
    result={'modo':'definitiva','competencia':competencia,'titulos_boletos':len(normalized),'chaves_canonicas':len(recon),'conciliados':counts.get('CONCILIADO',0),'pendencias':counts.get('PENDENTE',0),'publicacao_bi':status,'aviso':'AF, AR, boletos e ERP sao dominios distintos; mapeamento apenas de POC'}
    write_json(out/'resumo.json',result)
    return result
