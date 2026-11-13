# DOR 11 | CREDIN — créditos, boletos, AF/AR e ERP

**Foco:** UniCesumar/CREDIN: automatização da entrada de boletos de curto prazo EAD e reconciliação de **crédito a faturar (AF)**, **contas a receber (AR)**, títulos/boletos e saldo contábil. **CREDIN não é FIES**; a POC 02/FIES é referência de padrões de ingestão, nunca de regra financeira.

## Anexos realmente examinados

- `Controle CREDIN set.26.xlsx`, com 12 abas incluindo `Procedimentos`, `Balancete set.26`, `CREDIN AF PRES - 14B set.26`, `CREDIN AR PRES - 14 set.26`, `CREDIN AR EAD set.26`, `CREDIN AF EAD - 14B set.26`, `CREDIN AF EAD set.26`, `Movimentação recuperações` e `Aging`.
- ZIP de posição CREDIN com **9 XLS**: relatórios 14 (cinco) e 14B (quatro), cobrindo CP/LP de presencial/medicina.
- ZIP 72666: um CSV `relatorio_72666_expd_1523554_20261002121000.csv`, **8.205 registros** mais cabeçalho, 60 colunas, delimitador `;`, codificação Windows-1252. Entre elas `NOSSO_NUMERO`, `CODIGO_RA`, `PARCELA`, `VALOR_TITULO`, `VALOR_PAGO`, `VENCIMENTO`, `DATA_COMPETENCIA`.

**Atenção:** 14/14B em `.xls` não são lidos diretamente pelo laboratório; para integração real é necessária conversão oficial autorizada com controle de linhas/filtros. O CSV 72666 foi inspecionado no nível de layout; **nenhuma linha real foi incorporada**.

## Duas soluções

- [`solucao_paliativa/`](solucao_paliativa/): ingestão automatizável de CSV com subset de campos 72666, verificação de cabeçalhos, chave, duplicidades, quarentena, controle, hash e reexecução idempotente.
- [`solucao_definitiva/`](solucao_definitiva/): quatro domínios separados (72666, AR/14, AF/14B, ERP), conciliação por RA sintética, divergências explícitas e publicação no BI bloqueada em caso de diferença.

## Execução

```powershell
cd .\dor_11
.\executar_demo.ps1
# ou
py -3 .\main.py --modo paliativa
py -3 .\main.py --modo definitiva
py -3 -m unittest discover -s tests -v
```

As saídas `saida_demo/` têm apenas matrículas fictícias `RA-FICT-*`; **não executar com dados reais sem mascaramento e permissão corporativa**. O campo `SALDO_ILUSTRATIVO` é `VALOR_TITULO - VALOR_PAGO` para a demo, sem assumir tratamentos contábeis de repasses, descontos, baixa, ajustes e renegociação.
