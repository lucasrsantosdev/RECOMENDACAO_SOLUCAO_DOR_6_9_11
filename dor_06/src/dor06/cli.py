import argparse,json
from pathlib import Path
from .pdd import paliativa,definitiva

def main():
    parser=argparse.ArgumentParser(description='Dor 06 - PDD com curvas demonstrativas')
    parser.add_argument('--modo',choices=['paliativa','definitiva','ambos'],default='ambos')
    parser.add_argument('--saida',default='saida_demo')
    args=parser.parse_args();base=Path(__file__).resolve().parents[2]
    data=base/'dados_sinteticos';out=base/args.saida
    if args.modo in ('paliativa','ambos'):
        print('PALIATIVA:',json.dumps(paliativa(data/'carteira_202609.csv',data/'curvas_demo.csv',data/'controle_demo.csv',out/'paliativa'),ensure_ascii=False))
    if args.modo in ('definitiva','ambos'):
        print('DEFINITIVA:',json.dumps(definitiva(data/'eventos_carteira.csv',data/'curvas_demo.csv',out/'definitiva'),ensure_ascii=False))
