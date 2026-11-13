# Contratos sintéticos e contratos reais a pactuar

| Camada | Chave | Campos | Fonte na demo | Confirmação real pendente |
|---|---|---|---|---|
| Carteira | `TITULO_ID` | marca, modalidade, vencimento, saldo | `carteira_202609.csv` | origem oficial e unidade monetária |
| Curva | `MARCA,MODALIDADE,FAIXA,VERSAO` | taxa, vigência | `curvas_demo.csv` | categoria oficial, escalas e versionamento |
| Evento | `EVENTO_ID` | título, data efetiva, data conhecida, tipo, delta | `eventos_carteira.csv` | CDC e chave de origem |
| Controle | `MARCA` + competência | total esperado | `controle_demo.csv` | extrato contábil oficial/conta |

Cálculo **somente demonstrativo**: `PDD = saldo_aberto × taxa_ilustrativa` arredondado a centavos. Faixas: a vencer, 1–30, 31–60, 61–90, 91–120 e 121+. Não representa curva oficial nem necessariamente atende IFRS 9/CPC 48.
