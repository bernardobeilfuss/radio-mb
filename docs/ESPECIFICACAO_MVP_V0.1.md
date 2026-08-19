# Especificação Funcional — Rádio MB MVP v0.1

## 1. Objetivo

Entregar uma primeira versão executável da Rádio MB para validar o fluxo completo antes do deploy na VPS e antes da implantação nas 6 lojas.

Loja piloto definida: **Megashop Santo Ângelo** (`megashop`).

Fluxo-alvo:

VPS -> API/grade -> Player Web -> computador da loja -> cabo de áudio -> amplificador -> caixas.

## 2. Escopo funcional do MVP

### Player da loja

- acessar por URL contendo o identificador da loja;
- carregar automaticamente a programação vigente;
- exibir status online/offline;
- exibir faixa/chamada atual;
- tocar áudio sem permitir escolha de repertório pelo gerente;
- enviar heartbeat periódico ao servidor;
- registrar início e término das execuções;
- manter cache local de emergência para fallback offline.

### Backend

- cadastro das 6 lojas;
- catálogo de áudios;
- distinção entre música, campanha e institucional;
- metadados de licença para músicas;
- níveis de energia de 1 a 5;
- grade por faixa de horário;
- campanhas com início/fim e frequência;
- seleção da próxima mídia;
- regra anti-repetição;
- log de execução por loja;
- heartbeat e status das lojas.

### Compliance

Nenhuma música poderá ser marcada como apta para execução sem:

- título;
- artista;
- fonte;
- URL da fonte;
- tipo de licença;
- data de verificação;
- evidência/documento da licença;
- status de validação.

O sistema deve bloquear músicas sem `license_status = approved`.

## 3. Entidades

### Store

- id
- slug
- name
- city
- active
- last_heartbeat_at

### Media

- id
- type: music | campaign | institutional
- title
- artist
- file_url
- duration_seconds
- energy_level
- active

### License

- media_id
- source
- source_url
- license_type
- verified_at
- evidence_path
- license_status: pending | approved | rejected
- notes

### ScheduleRule

- id
- start_time
- end_time
- energy_min
- energy_max
- days_of_week

### Campaign

- media_id
- starts_at
- ends_at
- interval_minutes
- store_ids

### PlaybackLog

- id
- store_id
- media_id
- started_at
- ended_at
- source: online | fallback

## 4. Regras de programação

1. Música sem licença aprovada nunca entra na fila.
2. Campanha ativa tem prioridade quando atingir seu intervalo configurado.
3. Fora de campanha, selecionar música compatível com a energia do horário.
4. Evitar repetir a mesma faixa dentro de 3 horas.
5. Evitar repetir o mesmo artista em sequência.
6. Em indisponibilidade do servidor, tocar cache local aprovado.

## 5. API mínima

- `GET /health`
- `GET /api/stores`
- `GET /api/player/{store_slug}/next`
- `POST /api/player/{store_slug}/heartbeat`
- `POST /api/player/{store_slug}/playback/start`
- `POST /api/player/{store_slug}/playback/end`

No MVP inicial, os dados podem permanecer em memória/arquivo local apenas para validar comportamento. PostgreSQL entra antes do deploy produtivo.

## 6. Critérios de aceite do MVP local

- backend inicia sem erro;
- `/health` responde `ok`;
- player abre no navegador;
- player identifica a Megashop;
- player consulta `/next`;
- músicas sem licença aprovada são ignoradas;
- heartbeat aparece no backend para `megashop`;
- execução é registrada;
- ausência de conexão não trava o player;
- nenhum controle de escolha de faixa é exposto ao gerente.

## 7. Fora deste ciclo

- deploy na VPS;
- autenticação administrativa completa;
- geração de voz por IA;
- importador automático de catálogos CC0;
- painel administrativo completo;
- relatórios avançados;
- multi-tenant;
- integração com ERP.

## 8. Próximo gate

Somente depois de o MVP local passar nos critérios acima:

1. trocar armazenamento temporário por PostgreSQL;
2. implementar painel administrativo;
3. cadastrar catálogo piloto de 50–100 faixas aprovadas;
4. preparar deploy na VPS;
5. pilotar na Megashop Santo Ângelo;
6. executar CHECK do PDCA.
