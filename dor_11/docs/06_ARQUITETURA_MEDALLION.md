# Plano Medallion D11 — versão hipotética

| Camada | Domínios separados | Regras |
|---|---|---|
| RAW | 14/14B/72666, contratos, razão/ERP | Preservar origem, data e filtros |
| Bronze | boleto, dívida AF, AR, lançamentos, crosswalk | IDs versionados e contratos |
| Silver | `fato_credito_af`, `fato_titulo`, `fato_recebimento`, `fato_razao` | Cardinalidade explícita, status e recortes CP/LP |
| Gold | reconciliação fonte ↔ operação ↔ contábil | Gate bloqueia divergência, permite BI só após aceite |

**Risco especial:** balancete é agregado por conta; a ponte RA↔razão da POC não significa que o ERP real tenha RA. Validar chaves e join antes de construir Silver.
