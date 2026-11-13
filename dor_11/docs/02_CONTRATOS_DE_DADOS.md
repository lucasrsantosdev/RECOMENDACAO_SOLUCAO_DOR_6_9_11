# Contratos de dados e granularidade — D11

| Origem | Chave de demonstração | Campos | Lacunas |
|---|---|---|---|
| 72666 CSV | `NOSSO_NUMERO+CODIGO_RA+PARCELA` | `VALOR_TITULO`, `VALOR_PAGO`, `VENCIMENTO`, `DATA_COMPETENCIA` | Confirmar unicidade por negociação e data movimento; descontos/repasses e anulações |
| 14 AR | `RA` (agregado na demo) | `SALDO_AR`, modalidade | Relação título-posição real e múltiplos títulos por aluno |
| 14B AF | `RA` (agregado na demo) | bolsa concedida, dívida gerada, status | Dívida a gerar, bolsa, duração e eventos de faturamento |
| ERP/balancete | `RA` (apenas demo; provavelmente NÃO chave contábil real) | saldo contábil | Conta, centro de custo, competência, lote e granularidade de lançamento |

### Caveats de modelagem

- A conciliação demonstrativa utiliza `RA` como chave de controle inventada. **Nunca fazer join real do balancete por RA sem evidência de detalhe contábil**; balancete geralmente é agregado por conta, exigindo ponte documento/lote e reconciliação hierárquica.
- `SALDO_ILUSTRATIVO = VALOR_TITULO - VALOR_PAGO` é apenas exemplo de aritmética; não incluir como fórmula contábil homologada.
- `BOLSA_CONCEDIDA`, `DIVIDA_GERADA`, `A_GERAR`, `COBRANCA_FATURADA`, `COBRANCA_ABERTA`, `VALOR_REPASSE` possuem semânticas potencialmente diferentes; fórmula/tolerância deve vir do time financeiro.
- O arquivo 72666 é relatado como EAD CP; não extrapolar para presencial/medicina ou longo prazo.
