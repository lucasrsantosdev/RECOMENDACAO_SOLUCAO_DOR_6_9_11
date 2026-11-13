# Plano Medallion D06 — versão hipotética

| Camada | Entrada e chave | Política de dado | Produto |
|---|---|---|---|
| RAW | extrações CAR, curvas/controle e ERP com batch_id/hash | Append-only, acesso restrito | blob e manifesto |
| Bronze | schema por fonte, CDC, ingestion_timestamp | Histórico com versão por chave | tabelas Bronze isoladas |
| Silver | título, evento, carteira, curva versionada | Identidade e regra auditáveis | exposição por referência |
| Gold | posição PDD e aging por referência e curva | Fechamento imutável; reconciliação e ownership | relatório e visão semântica |

**Ainda não há execução Delta/Databricks nem esquema corporativo validado.**
