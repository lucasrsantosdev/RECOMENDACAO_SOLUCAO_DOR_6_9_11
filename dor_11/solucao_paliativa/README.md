# Paliativa — carga controlada de boletos CREDIN (72666)

**Problema abordado imediatamente:** recebimento recorrente do relatório 72666 EAD CP, processamento manual e risco de erro de fórmulas/filtros em planilha.

**Proposta operacional:** exportação do legado em canal autorizado → pasta de aterrissagem de acesso restrito → job controlado de leitura CSV (`;`, UTF-8 ou Windows-1252) → validação de contrato e competência → deduplicação/segregação de conflitos → resumo financeiro, exceções e check de totais → entrega para conferência. Os dados sensíveis do original devem permanecer em armazenamento autorizado; não subir ao Git.

**Executável hoje (somente fictício):** `py -3 main.py --modo paliativa`; arquivos `silver_boletos.csv`, `quarentena.csv`, `controle.csv`, `manifest_lotes.json` e `resumo.json`.

**Observações:** 72666 pode conter títulos com juros/multa, deduções, repasses e negociações; a fórmula nominal básica da POC não representa saldo devedor oficial. A chave `NOSSO_NUMERO + CODIGO_RA + PARCELA` é **hipótese**; validar se é unique e estável com TI. Para agendar: Task Scheduler, ADF ou job Databricks, apenas após redesenho de acesso, segredos, logs, SLA e política de reprocessamento.

## Executar separadamente

```powershell
cd .\solucao_paliativa
.\executar.ps1
```

**Código-fonte modular:** `../src/dor11/credin.py` (motor e regras); `../src/dor11/io_utils.py` (integridade e contratos); `executar.py` (entrada de execução independente).

**Filtro essencial:** `--competencia 202609` (padrão). O relatório de origem pode conter dezenas de competências; o processo preserva auditoria de distribuição por mês em `auditoria_competencias.csv` e só calcula total do mês selecionado.
