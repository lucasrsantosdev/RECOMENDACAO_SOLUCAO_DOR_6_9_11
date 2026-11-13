import argparse,json
from pathlib import Path
from .credin import paliativa,definitiva

def main():
    parser=argparse.ArgumentParser(description='Dor 11 - CREDIN/boletos/AF/AR/ERP')
    parser.add_argument('--modo',choices=['paliativa','definitiva','ambos'],default='ambos')
    parser.add_argument('--saida',default='saida_demo')
    parser.add_argument('--competencia',default='202609')
    args=parser.parse_args();root=Path(__file__).resolve().parents[2];d=root/'dados_sinteticos';out=root/args.saida
    if args.modo in ('paliativa','ambos'):
        print('PALIATIVA:',json.dumps(paliativa(d/'boletos_72666_demo.csv',d/'controle_boletos_demo.csv',out/'paliativa',competencia=args.competencia),ensure_ascii=False))
    if args.modo in ('definitiva','ambos'):
        print('DEFINITIVA:',json.dumps(definitiva(d/'boletos_72666_demo.csv',d/'ar_14_demo.csv',d/'af_14b_demo.csv',d/'erp_demo.csv',out/'definitiva',competencia=args.competencia),ensure_ascii=False))
