# Definitiva — reconstrução histórica CAR

**Arquitetura-alvo:** Oracle/Gioconda (e fontes oficiais identificadas) → Azure Data Factory/ingestão autorizada → Databricks Raw (preservação original) → Bronze CDC/SCD2 e histórico de extração → Silver eventos e saldos canônicos → Gold fotos por `data_efetiva`, `data_conhecimento` e `competencia` → auditabilidade e BI.

**Implementado em Python local:** motor de eventos (`EMISSAO`, `PAGAMENTO`, `ESTORNO`, `AJUSTE`, `RENEGOCIACAO`, `CANCELAMENTO`), replay bitemporal, bloqueio de movimentos órfãos, controles de saldo negativo, trilha por evento, comparação e identificação de retroativos.

**Dependências para Databricks real:** PKs/FKs, procedures/DDL Oracle, semântica real de alteração e exclusão, extrações transacionais/cdc, controle de late arriving events, SCD2, protocolo Delta MERGE, Unity Catalog, retenção, SLA, conciliação contábil e testes em sandbox. O CSV de captura não substitui um log de eventos nativo.

## Executar separadamente

```powershell
cd .\solucao_definitiva
.\executar.ps1
```

**Código-fonte modular:** `../src/dor09/historico.py` (motor e regras); `../src/dor09/io_utils.py` (integridade e contratos); `executar.py` (entrada de execução independente).
