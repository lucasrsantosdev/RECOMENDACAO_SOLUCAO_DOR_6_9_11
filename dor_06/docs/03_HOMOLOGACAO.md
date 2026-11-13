# Cenários e aceite — D06

| Cenário | Expectativa | Demonstração |
|---|---|---|
| Taxa fora de 0–1, curva ausente, duplicidade de título, saldo negativo | Bloquear execução | Testes unitários |
| Duas capturas do mesmo lote com arquivos diferentes | Bloquear substituição | `add_manifest()` |
| Reconciliação de carteira com controle | Delta zero por marca | `reconciliacao.csv` |
| Pagamento conhecido somente em outubro, efetivo setembro | Reproduzir PDD de setembro conhecida em setembro **e** PDD revisada | `gold_pdd_*` |
| Política oficial e dados reais | PDD oficial reproduzida por competência | **Pendente de TI/Contabilidade** |

O status `APROVADA_DEMO` significa apenas **controle sintético coerente**, não aprovação contábil.
