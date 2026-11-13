# Rastreabilidade de solução — D11

| Requisito | Implementação POC | Evidência |
|---|---|---|
| Recepção 72666 | `credin.load_72666` | teste de cabeçalho/encoding |
| Chave, duplicidade, tipos | `credin.normalize_bills` | testes de chave, conflito e valores |
| Arquivo e processamento | `credin.paliativa` | manifesto, controle e resumo |
| Separar domínios AF/AR/ERP | `credin.reconcile` | teste `test_af_not_compared_to_ar` |
| Gate BI em divergências | `credin.definitiva` | teste `test_definitiva_bi_blocked_on_gaps` e `pendencias.csv` |
| Regra oficial e integração real | Não implementado | Solicitações TI/Financeiro |
