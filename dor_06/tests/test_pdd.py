import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dor06.pdd import band,load_curves,evaluate,portfolio_from_events,paliativa,definitiva
from dor06.io_utils import read_csv
D=Path(__file__).resolve().parents[1]/'dados_sinteticos'
class PDDTests(unittest.TestCase):
    def test_aging(self):
        self.assertEqual(band('2026-09-30','2026-09-30'),'A_VENCER')
        self.assertEqual(band('2026-08-15','2026-09-30'),'31_60')
    def test_paliativa_aceita_controle(self):
        with tempfile.TemporaryDirectory() as d:
            r=paliativa(D/'carteira_202609.csv',D/'curvas_demo.csv',D/'controle_demo.csv',d)
            self.assertEqual(r['validacao_controle'],'APROVADA_DEMO')
    def test_idempotencia_mesmo_arquivo(self):
        with tempfile.TemporaryDirectory() as d:
            p=paliativa(D/'carteira_202609.csv',D/'curvas_demo.csv',D/'controle_demo.csv',d)
            q=paliativa(D/'carteira_202609.csv',D/'curvas_demo.csv',D/'controle_demo.csv',d)
            self.assertEqual(p,q)
    def test_evento_retroativo_altera_reprocessamento(self):
        rows=read_csv(D/'eventos_carteira.csv',('TITULO_ID',))
        a=portfolio_from_events(rows,'2026-09-30','2026-09-30')
        b=portfolio_from_events(rows,'2026-09-30','2026-10-07')
        self.assertEqual(next(x for x in a if x['TITULO_ID']=='T-001')['SALDO_ABERTO'],'1000.00')
        self.assertEqual(next(x for x in b if x['TITULO_ID']=='T-001')['SALDO_ABERTO'],'800.00')
    def test_taxa_invalida(self):
        curves,_=load_curves(D/'curvas_demo.csv')
        row=dict(TITULO_ID='TESTE',MARCA='UNIASSELVI',MODALIDADE='EAD',VENCIMENTO='2026-06-01',SALDO_ABERTO='-3.00')
        with self.assertRaises(ValueError):evaluate([row],curves,'2026-09-30')
    def test_falta_curva_rejeitada(self):
        curves,_=load_curves(D/'curvas_demo.csv')
        row=dict(TITULO_ID='T99',MARCA='SEM',MODALIDADE='EAD',VENCIMENTO='2026-06-01',SALDO_ABERTO='100')
        with self.assertRaises(ValueError):evaluate([row],curves,'2026-09-30')
    def test_definitiva_calcula_impacto(self):
        with tempfile.TemporaryDirectory() as d:
            r=definitiva(D/'eventos_carteira.csv',D/'curvas_demo.csv',d)
            self.assertNotEqual(r['pdd_original'],r['pdd_reprocessada'])
if __name__=='__main__':unittest.main()
