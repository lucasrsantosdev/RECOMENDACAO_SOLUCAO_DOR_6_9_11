# Critérios de homologação — D11

| Caso | Resultado esperado na demo | Homologação real |
|---|---|---|
| CSV 72666 UTF-8 / CP1252 | Leitura por formato e colunas exigidas | Entrega oficial e encoding fixado |
| Número/RA/parcela duplicados idênticos | Registrar em quarentena, não duplicar somatório | Confirmar chave real e tratamento de exportação duplicada |
| Duplicado com valor conflitante | Bloquear resolução automática | Canal com owner da origem |
| Valor negativo ou pago acima do título | Quarentena por contrato ilustrativo | Validar desconto, estorno e juros |
| Totais do lote divergentes | Paliativa bloqueada | Confirmar balancete/controle e tolerance |
| Saldo AF diferente de AR | Não sinalizar erro automaticamente | Regras de geração da dívida e conciliação AF/AR |
| Ausência/diferença AR/ERP | Gate `publicacao_bi=BLOQUEADA` | Conciliação contábil e aceite |
| Boletos/controle/ERP reais | Não executado | Sandbox autorizado e comparação por competência e conta |
