# Plano Medallion D09 — versão hipotética

| Camada | Objeto | Garantia principal |
|---|---|---|
| RAW | arquivos, extrato CDC e manifesto | Integridade original por lote |
| Bronze | registros por data de captura e versão do evento | Não sobrescrever histórico, tombstone explícito |
| Silver | título / pagamento / baixa / ajuste / renegociação | Vigência do evento e data conhecida |
| Gold | snapshot no fechamento, posição recalculada, aging e reconciliação | Replay bitemporal e gate de qualidade |

**Confirmar** se Oracle/Gioconda pode fornecer CDC/eventos confiáveis. Snapshots XLS/CSV não garantem log completo de eventos.
