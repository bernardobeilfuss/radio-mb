# Rádio MB

Rádio indoor própria do Grupo MB para as 6 lojas, com player web centralizado na VPS, catálogo musical documentado e inserções comerciais geradas por IA.

## Objetivos

- reduzir risco relacionado ao ECAD por meio de repertório com direitos/licenças documentados;
- manter ambiente de loja animado e adequado ao varejo;
- não tocar funk;
- operar sem intervenção dos gerentes;
- permitir programação e campanhas centralizadas;
- executar no computador da loja via navegador e saída de áudio para o amplificador existente.

## Arquitetura alvo

VPS -> API/grade -> Player Web -> computador da loja -> cabo de áudio -> amplificador -> caixas.

## MVP v0.1

- player web;
- painel administrativo;
- cadastro das 6 lojas;
- catálogo CC0/domínio público validado;
- registro de licença/evidência por faixa;
- níveis de energia;
- programação por horário;
- campanhas com início/fim e frequência;
- logs de execução;
- monitor online/offline;
- fallback offline.

## Método

Desenvolvimento e implantação em ciclos PDCA.

Consulte `docs/PLANO.md` e `docs/COMPLIANCE.md`.
