# D09 — Casos, testes e critérios de aceite

- **Idempotência:** recapturar o mesmo arquivo com mesmo ID não altera histórico; trocar bytes sob mesmo ID é bloqueado (`test_reject_same_id_new_content`).
- **Raw alterada:** hash divergiu, rejeitar replay (`test_raw_tamper_blocked`).
- **Comparação:** uma linha ausente em nova foto é marcada como ausência, não como exclusão (`test_missing_is_not_delete`).
- **Retroativo:** pagamento efetivo 29/09, conhecido em outubro, não modifica posição **conhecida** 30/09; posição **recalculada** altera (`test_retroatividade`).
- **Órfão:** movimento sem título de origem bloqueado (`test_orphan_rejected`).
- **Real:** comparar relatório CAR oficial de 30/09 arquivado, mesmo relatório reextraído em outubro e razão contábil; explicar 100% das diferenças por evento/versionamento — **pendente**.
