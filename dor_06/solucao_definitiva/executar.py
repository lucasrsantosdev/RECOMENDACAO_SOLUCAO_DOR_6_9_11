"""Entrada independente para a solucao definitiva da Dor 06."""
import sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from dor06.cli import main
if __name__=='__main__':
    # O codigo fica em src/dor06, isolando a regra do launcher.
    sys.argv=[str(root/'main.py'),'--modo','definitiva']+sys.argv[1:]
    main()
