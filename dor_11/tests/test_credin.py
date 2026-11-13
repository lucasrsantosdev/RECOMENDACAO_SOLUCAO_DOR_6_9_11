import unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dor11.credin import normalize_bills,load_72666,paliativa,definitiva,reconcile,parse_due,parse_competence
D=Path(__file__).resolve().parents[1]/'dados_sinteticos'
class CredinTests(unittest.TestCase):
    def test_actual_72666_format_dates(self):
        self.assertEqual(parse_due('09/10/2023'),'2023-10-09')
        self.assertEqual(parse_competence('08/2023'),'202308')
    def test_multiplas_competencias_separadas(self):
        with tempfile.TemporaryDirectory() as d:
            raw=list(__import__('csv').DictReader((D/'boletos_72666_demo.csv').open(encoding='utf-8'),delimiter=';'))
            extra=dict(raw[0]);extra['NOSSO_NUMERO']='B-ANTERIOR';extra['DATA_COMPETENCIA']='08/2026'
            from dor11.io_utils import write_csv
            filepath=Path(d)/'boletos_mistos.csv'
            write_csv(filepath,raw+[extra],raw[0].keys())
            result=paliativa(filepath,D/'controle_boletos_demo.csv',Path(d)/'out')
            self.assertEqual(result['competencias_distintas'],2)
            self.assertEqual(result['titulos_validos'],4)
    def test_72666_header(self):
        rows,encoding=load_72666(D/'boletos_72666_demo.csv')
        self.assertEqual(len(rows),4)
    def test_normalize_and_sum(self):
        rows,_=load_72666(D/'boletos_72666_demo.csv')
        normalized,errors=normalize_bills(rows)
        self.assertEqual(len(normalized),4);self.assertEqual(errors,[])
        self.assertEqual(normalized[0]['SALDO_ILUSTRATIVO'],'800.00')
    def test_duplicate_conflict_quarantine(self):
        rows,_=load_72666(D/'boletos_72666_demo.csv')
        wrong=dict(rows[0]);wrong['VALOR_TITULO']='999.00'
        x,q=normalize_bills(rows+[wrong]);self.assertEqual(len(x),4)
        self.assertEqual(q[0]['CODIGO'],'CONFLITO_DE_CHAVE')
    def test_duplicate_identical_quarantine(self):
        rows,_=load_72666(D/'boletos_72666_demo.csv')
        x,q=normalize_bills(rows+[rows[0]])
        self.assertEqual(q[0]['CODIGO'],'DUPLICATA_IDENTICA')
    def test_invalid_negative(self):
        rows,_=load_72666(D/'boletos_72666_demo.csv')
        wrong=dict(rows[0]);wrong['VALOR_PAGO']='-1.00'
        _,q=normalize_bills([wrong]);self.assertEqual(q[0]['CODIGO'],'VALOR_OU_DATA_INVALIDA')
    def test_paliativa_control(self):
        with tempfile.TemporaryDirectory() as d:
            res=paliativa(D/'boletos_72666_demo.csv',D/'controle_boletos_demo.csv',d)
            self.assertEqual(res['status'],'APROVADO_DEMO')
    def test_idempotent_batch(self):
        with tempfile.TemporaryDirectory() as d:
            a=paliativa(D/'boletos_72666_demo.csv',D/'controle_boletos_demo.csv',d)
            b=paliativa(D/'boletos_72666_demo.csv',D/'controle_boletos_demo.csv',d)
            self.assertEqual(a,b)
    def test_definitiva_bi_blocked_on_gaps(self):
        with tempfile.TemporaryDirectory() as d:
            x=definitiva(D/'boletos_72666_demo.csv',D/'ar_14_demo.csv',D/'af_14b_demo.csv',D/'erp_demo.csv',d)
            self.assertEqual(x['publicacao_bi'],'BLOQUEADA')
            self.assertGreater(x['pendencias'],0)
    def test_af_not_compared_to_ar(self):
        bills=[{'RA':'TEST','SALDO_ILUSTRATIVO':'10.00'}]
        ar=[{'RA':'TEST','MODALIDADE':'EAD','SALDO_AR':'10.00'}]
        af=[{'RA':'TEST','MODALIDADE':'EAD','BOLSA_CONCEDIDA':'500.00','DIVIDA_GERADA':'200.00'}]
        erp=[{'RA':'TEST','MODALIDADE':'EAD','SALDO_CONTABIL':'10.00'}]
        rows,counts=reconcile(bills,ar,af,erp)
        self.assertEqual(rows[0]['STATUS'],'CONCILIADO')
    def test_missing_erp_not_silent(self):
        bills=[{'RA':'TEST','SALDO_ILUSTRATIVO':'10.00'}]
        ar=[{'RA':'TEST','MODALIDADE':'EAD','SALDO_AR':'10.00'}]
        af=[{'RA':'TEST','MODALIDADE':'EAD','BOLSA_CONCEDIDA':'10.00','DIVIDA_GERADA':'10.00'}]
        rows,counts=reconcile(bills,ar,af,[])
        self.assertIn('SEM_ERP',rows[0]['MOTIVOS'])
if __name__=='__main__':unittest.main()
