# Paliativa — cálculo controlado por lote

Fluxo: exportação autorizada (não implementada) → arquivo de entrada → verificação `TITULO_ID` único, saldo não negativo e curva completa → cálculo ilustrativo → totais por marca → registro de hashes e exceções. Imutabilidade é **por ID de lote dentro da demo**, não WORM.

## Entrada demonstrativa

- `dados_sinteticos/carteira_202609.csv`: `TITULO_ID`, `MARCA`, `MODALIDADE`, `VENCIMENTO` (ISO), `SALDO_ABERTO`.
- `dados_sinteticos/curvas_demo.csv`: taxa decimal de 0 a 1, categoria de atraso, versão.
- `dados_sinteticos/controle_demo.csv`: saldo esperado por marca.

## Entrega e decisão

`gold_pdd_ilustrativa.csv`, `reconciliacao.csv`, `manifest_entrada.json`, `resumo.json`. Processo pode ser agendado futuramente por job autorizado; neste laboratório roda manualmente. **Paliativa não corrige base de origem e não homologou o cálculo oficial.**

## Executar separadamente

```powershell
cd .\solucao_paliativa
.\executar.ps1
```

**Código-fonte modular:** `../src/dor06/pdd.py` (motor e regras); `../src/dor06/io_utils.py` (integridade e contratos); `executar.py` (entrada de execução independente).
