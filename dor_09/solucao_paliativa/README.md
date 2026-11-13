# Paliativa — foto CAR com integridade

1. Exportar relatório CAR por competência e data/hora em canal autorizado; preservar arquivo bruto e hash do lote.
2. Usar captura com ID único e não substituir arquivos históricos; manter manifesto, contagens e valor total.
3. Comparar posições: títulos novos, alterados, inalterados e ausentes na segunda foto.
4. Abrir fila de justificativas para pagamentos, baixas, renegociações e ajustes posteriores.

**Implementado na demo:** recepção de dois CSVs fictícios, imutabilidade lógica por ID, verificação de arquivo RAW, análise de diferenças, saídas CSV/JSON. **Não implementado:** agendamento de produção, extração Gioconda, serviço de object lock e validação de volume total do relatório. A existência de uma linha em uma foto e ausência em outra NÃO constitui prova de exclusão física.

## Executar separadamente

```powershell
cd .\solucao_paliativa
.\executar.ps1
```

**Código-fonte modular:** `../src/dor09/historico.py` (motor e regras); `../src/dor09/io_utils.py` (integridade e contratos); `executar.py` (entrada de execução independente).
