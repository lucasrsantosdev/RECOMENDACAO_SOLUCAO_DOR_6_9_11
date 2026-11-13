import csv
import hashlib
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation
def read_csv(path, required=()):
    path=Path(path)
    with path.open('r',encoding='utf-8-sig',newline='') as handle:
        rd=csv.DictReader(handle,delimiter=';')
        if not rd.fieldnames or not set(required).issubset(set(rd.fieldnames)):
            raise ValueError(f'Contrato invalido em {path.name}. Campos obrigatorios ausentes: {sorted(set(required)-set(rd.fieldnames or []))}')
        return list(rd)
def write_csv(path, rows, fields):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as handle:
        w=csv.DictWriter(handle,fieldnames=fields,delimiter=';',lineterminator='\n',extrasaction='ignore')
        w.writeheader();w.writerows(rows)
def write_json(path, data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True),encoding='utf-8')
def cents(value):
    try:
        return int((Decimal(str(value).strip().replace(',','.'))*100).quantize(Decimal('1')))
    except (InvalidOperation,ValueError):raise ValueError(f'Valor monetario invalido') from None
def br(c):return f'{c/100:.2f}'
def sha(data):return hashlib.sha256(data).hexdigest()
def digest(path):return sha(Path(path).read_bytes())
def add_manifest(path,source,id):
    """Imutabilidade demonstrativa por ID, metadados e hash. Nao substitui WORM corporativo."""
    path=Path(path); source=Path(source);path.parent.mkdir(parents=True,exist_ok=True)
    current=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    entry={'arquivo':source.name,'sha256':digest(source),'bytes':source.stat().st_size}
    if id in current and current[id]!=entry:raise ValueError('Capture ID ja existe com conteudo divergente: bloqueado')
    new=id not in current
    if new:
        current[id]=entry;write_json(path,current)
    return entry,new
