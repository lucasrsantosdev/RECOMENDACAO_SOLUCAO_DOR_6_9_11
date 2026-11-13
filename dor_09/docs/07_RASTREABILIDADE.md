# Matriz de rastreabilidade — D09

| Requisito | Código | Evidência |
|---|---|---|
| RAW preservada | `historico.capture` | `raw/*.csv`, `manifests.json`, teste de adulteração |
| Fotos distintas | `historico.compare_files` | `comparacao_fotos.csv` |
| Ausência não é exclusão | `compare_files` | teste de classificação |
| Replay e temporalidades | `historico.replay` | `gold_fechamento_original.csv`, `gold_posicao_recalculada.csv` |
| Eventos órfãos | `replay` | testes de bloqueio |
| SQL real / CDC / ADF | Não implementado | DDL/owner/contrato pendente |
