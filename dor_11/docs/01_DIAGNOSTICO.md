# D11 — Dor de Crédito/CREDIN

**Relato:** crédito estudantil privado CREDIN com controles manuais, dificuldade de demonstrar posição consolidada de saldo aberto versus dívida gerada e boletos emitidos, renegociações/baixas e conciliações contábeis. Distinguir curto e longo prazo e modalidades EAD, presencial e medicina.

**Evidências do anexo:** existe planilha consolidada set/26 com AF/AR e balancete, fontes 14/14B em `.xls` e 72666 em `.csv`. Nomes das abas sugerem dimensões AF/AR, mas **não comprovam o relacionamento transacional**.

**Prioridade de análise:** 14 (posição AR CP), 14B (AF LP), 72666 (boletos CP EAD); depois as respectivas posições do controle e do balancete. No anexo 14/14B existem arquivos separados por modalidade; confirmar com dono da origem o recorte completo de CP/LP/EAD/PRES/MED.

**Causa-raiz candidata:** controles agregados em Excel não estão vinculados a identificadores, versões e fontes de verdade única por atributo, combinados com lacuna de automação para extrações frequentes e diferenças de competência/data de captura.

## Achado de perfil de fonte (inspeção estrutural 13/11/2026)

O CSV 72666 possui **8.205 registros, distribuídos por 79 competências**, embora o ZIP seja rotulado como setembro/2026. Apenas **92 registros possuem competência 202609** no campo `DATA_COMPETENCIA`. Existem **8.203 linhas com `VALOR_PAGO` vazio**. Esses números são de perfil da extração fornecida, não saldos homologados.

**Conclusão técnica:** separar `data_captura` de `competencia`, não atribuir o arquivo inteiro ao mês do ZIP e validar se `VALOR_PAGO` vazio significa sem pagamento ou incompletude do campo. O módulo paliativo filtra por competência e gera `auditoria_competencias.csv` antes de produzir os controles.
