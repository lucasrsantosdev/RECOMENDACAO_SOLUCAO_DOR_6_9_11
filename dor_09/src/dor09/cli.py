import argparse,json
from pathlib import Path
from .historico import paliativa,definitiva

def main():
    parser=argparse.ArgumentParser(description='Dor 09 - foto historica de CAR e replay')
    parser.add_argument('--modo',choices=['paliativa','definitiva','ambos'],default='ambos')
    parser.add_argument('--saida',default='saida_demo')
    a=parser.parse_args();root=Path(__file__).resolve().parents[2];d=root/'dados_sinteticos';out=root/a.saida
    if a.modo in ('paliativa','ambos'):
        print('PALIATIVA:',json.dumps(paliativa(d/'car_20260930.csv',d/'car_20261005.csv',out/'paliativa'),ensure_ascii=False))
    if a.modo in ('definitiva','ambos'):
        print('DEFINITIVA:',json.dumps(definitiva(d/'eventos_car.csv',out/'definitiva'),ensure_ascii=False))
