import unittest,tempfile,sys,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dor09.historico import capture,compare_files,paliativa,replay,definitiva,validate_snapshot
from dor09.io_utils import read_csv
D=Path(__file__).resolve().parents[1]/'dados_sinteticos'
class SnapshotTests(unittest.TestCase):
    def test_snapshot_immutable_and_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            one=capture(D/'car_20260930.csv','CAP1',d)
            two=capture(D/'car_20260930.csv','CAP1',d)
            self.assertTrue(one['nova']);self.assertFalse(two['nova'])
    def test_reject_same_id_new_content(self):
        with tempfile.TemporaryDirectory() as d:
            capture(D/'car_20260930.csv','CAP1',d)
            with self.assertRaises(ValueError):capture(D/'car_20261005.csv','CAP1',d)
    def test_raw_tamper_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            capture(D/'car_20260930.csv','CAP1',d)
            (Path(d)/'raw'/'CAP1.csv').write_text('adulterado')
            with self.assertRaises(ValueError):capture(D/'car_20260930.csv','CAP1',d)
    def test_missing_is_not_delete(self):
        with tempfile.TemporaryDirectory() as d:
            r=compare_files(D/'car_20260930.csv',D/'car_20261005.csv',d)
            self.assertEqual(r['resumo']['AUSENTE_NA_FOTO_NOVA_NAO_EXCLUSAO'],1)
    def test_retroatividade(self):
        events=read_csv(D/'eventos_car.csv',('EVENTO_ID',))
        old=replay(events,'2026-09-30','2026-09-30')
        later=replay(events,'2026-09-30','2026-10-05')
        self.assertEqual(next(r for r in old if r['TITULO_ID']=='CAR-001')['SALDO'],'1000.00')
        self.assertEqual(next(r for r in later if r['TITULO_ID']=='CAR-001')['SALDO'],'800.00')
    def test_orphan_rejected(self):
        events=read_csv(D/'eventos_car.csv',('EVENTO_ID',))
        bogus=dict(events[3]);bogus['EVENTO_ID']='ORPHAN';bogus['TITULO_ID']='MISSING'
        with self.assertRaises(ValueError):replay([bogus],'2026-09-30','2026-10-05')
    def test_definitiva_generates_delta(self):
        with tempfile.TemporaryDirectory() as d:
            x=definitiva(D/'eventos_car.csv',d)
            self.assertEqual(x['delta'],'-100.00')
    def test_paliativa_duas_fotos(self):
        with tempfile.TemporaryDirectory() as d:
            result=paliativa(D/'car_20260930.csv',D/'car_20261005.csv',d)
            self.assertEqual(len(result['capturas']),2)
if __name__=='__main__':unittest.main()
