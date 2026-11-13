# Matriz de rastreabilidade — D06

| Requisito | Módulo | Teste/evidência |
|---|---|---|
| Curva versionada | `pdd.load_curves` | `test_taxa_invalida` e manifesto |
| Aging | `pdd.band` | `test_aging` |
| Controle marca | `pdd.control` | `test_paliativa_aceita_controle`, `reconciliacao.csv` |
| Eventos retroativos | `pdd.portfolio_from_events` | `test_evento_retroativo_altera_reprocessamento` |
| Reprodutibilidade | `pdd.definitiva` | `gold_pdd_*`, manifesto com hash |
| Homologação oficial | Não implementada | Solicitação TI pendente |
