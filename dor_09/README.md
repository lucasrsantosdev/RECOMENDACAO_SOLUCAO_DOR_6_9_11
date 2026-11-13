# DOR 09 | CAR — histórico de saldos, fotos e retroatividade

**Problema:** um relatório CAR emitido hoje pode revelar dados alterados após o fechamento anterior, impedindo a reprodução de uma posição histórica. Não atribuímos erro ao Gioconda sem rastrear o processamento.

> **Anexo:** `Dor 09.zip` não continha documentos; apenas pastas vazias. A POC foi construída com base nas reuniões/POCs anteriores e casos sintéticos. Sem alegação de que a extração REAL foi analisada.

- [`solucao_paliativa/`](solucao_paliativa/): capturar relatórios de posição em `RAW`, manifestos SHA-256, controle idempotente por ID e comparação entre duas fotos; não presumir exclusão por ausência.
- [`solucao_definitiva/`](solucao_definitiva/): replay bitemporal por evento, fechamento original vs posição revisada e trilha do impacto retroativo; proposta Raw/Bronze/Silver/Gold para Databricks.

## Executar

```powershell
cd .\dor_09
.\executar_demo.ps1
# ou
py -3 .\main.py --modo paliativa
py -3 .\main.py --modo definitiva
py -3 -m unittest discover -s tests -v
```

Arquivos de demonstração em `saida_demo/`. O módulo histórico diferencia **posição efetiva** (competência) de **conhecimento do evento** (quando foi recebido). Não oferece CDC Oracle real, cópia WORM corporativa, exclusões confirmadas ou homologação CAR.
