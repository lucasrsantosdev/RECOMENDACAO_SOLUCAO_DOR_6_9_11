# Definitiva — PDD reproduzível e governada

Fluxo alvo: Gioconda/Lyceum + ERP autorizados → RAW imutável e catálogo → Bronze versões/CDC → Silver carteira, baixas, recuperações e condições financeiras → Gold aging, PDD e memória de cálculo por competência → fechamento mensal congelado e BI após gate.

**O que está implementado:** motor local de projeção por eventos sintéticos com duas temporalidades (`EFETIVO_EM`, `CONHECIDO_EM`), comparação de fechamento e retroatividade, cálculo de PDD demonstrativa usando curva versionada.

**O que depende de TI:** origem/tabelas, motor real PDD, taxa por segmentação/status, curva trimestral aplicada mensalmente (hipótese do diagnóstico), reversões e recuperações, políticas de histórico e liberação contábil. Não há Delta/PySpark nem conectores reais neste repositório.

## Executar separadamente

```powershell
cd .\solucao_definitiva
.\executar.ps1
```

**Código-fonte modular:** `../src/dor06/pdd.py` (motor e regras); `../src/dor06/io_utils.py` (integridade e contratos); `executar.py` (entrada de execução independente).
