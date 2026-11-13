"""Entrada independente para a solucao paliativa da Dor 09."""
import sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from dor09.cli import main
if __name__=='__main__':
    # O codigo fica em src/dor09, isolando a regra do launcher.
    sys.argv=[str(root/'main.py'),'--modo','paliativa']+sys.argv[1:]
    main()
