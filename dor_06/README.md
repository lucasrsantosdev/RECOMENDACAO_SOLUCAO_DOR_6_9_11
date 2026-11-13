# DOR 06 | PDD / provisão para perdas — FOURD × VITRU

**Problema:** dependência de planilhas de curva, apuração por marca/modalidade e ausência de trilha íntegra de parâmetros, bases e versões do fechamento.

- **Paliativa** em [`solucao_paliativa/`](solucao_paliativa/): recebe carteira sintética e curva versão `DEMO-202609-V1`, valida faixa/taxa/chave, calcula aging e PDD ilustrativa, confronta saldo esperado e preserva hash de insumos.
- **Definitiva** em [`solucao_definitiva/`](solucao_definitiva/): simula histórico de eventos com data efetiva e data conhecida, calcula exposições no fechamento e posições revisadas, documenta a alteração retroativa da PDD ilustrativa.

**O que vimos nos anexos:** duas curvas 2026 com abas por modalidade (incluindo EAD, presencial, medicina, continuada, pós, tecnólogos), estrutura mensal 2023–2026. **O que NÃO sabemos:** fórmula/política oficial, base do denominador, posição da carteira, fator de escala, contas contábeis, sinal da PDD, vigência de curva, regra de renegociações e classificação dedutível/indedutível.

## Executar

```powershell
cd .\dor_06
.\executar_demo.ps1
# ou
py -3 .\main.py --modo paliativa
py -3 .\main.py --modo definitiva
py -3 -m unittest discover -s tests -v
```

Saídas demonstrativas em `saida_demo/paliativa/` e `saida_demo/definitiva/`. Nenhum valor de curva PDD real foi utilizado. Não usar o número demonstrativo para escrituração ou avaliação de perdas.

**Documentos:** `docs/01_DIAGNOSTICO.md`, `docs/02_CONTRATOS_DE_DADOS.md`, `docs/03_HOMOLOGACAO.md`, `docs/04_SOLICITACOES_TI.md`, `docs/05_SEGURANCA_LGPD.md`, `docs/07_RASTREABILIDADE.md`.
