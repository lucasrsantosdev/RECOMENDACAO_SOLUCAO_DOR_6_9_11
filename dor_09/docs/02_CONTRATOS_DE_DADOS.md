# Contratos a homologar — D09

| Entidade | Chave POC | Campos críticos | Origem real |
|---|---|---|---|
| Posição CAR | `TITULO_ID+captura_id` | competência, vencimento, saldo, status, marca, capturado em | A confirmar no relatório oficial |
| Eventos | `EVENTO_ID` | tipo, título, delta, data efetiva, data conhecida, referência do evento anterior | A confirmar no Oracle/CDC |
| Fechamento | `competencia+versao` | momento da publicação, arquivo hash, regra versão, total contábil | Financeiro/Contabilidade |
| Controle de carga | `captura_id` | origem, hash, bytes, qualidade, watermark | Orquestrador autorizado |

Regra essencial: `EFETIVO_EM` diferente de `CONHECIDO_EM`; para reconstrução “como era sabido em 30/09”, filtrar por ambas as datas. `EVENTO_ID` não pode ser repetido; exclusão só deve ser confirmada quando houver semântica de CDC ou declaração inequívoca de snapshot completo e consistente.
