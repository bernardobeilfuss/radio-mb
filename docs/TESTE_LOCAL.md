# Teste local — Rádio MB MVP v0.1

## Loja piloto

O teste inicial e o primeiro piloto de implantação serão feitos na **Megashop Santo Ângelo** (`megashop`).

## Pré-requisitos

- Python 3.11+
- navegador moderno

## Backend

No diretório `server`:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Suba a API:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Valide:

```text
http://localhost:8000/health
```

Resposta esperada:

```json
{"status":"ok","service":"radio-mb","version":"0.1.0"}
```

## Player

Sirva a pasta `apps/player` com um servidor HTTP simples:

```bash
python -m http.server 8080 --directory apps/player
```

Abra:

```text
http://localhost:8080/?loja=megashop&api=http://localhost:8000
```

Clique em `Iniciar Rádio`.

Como ainda não há arquivo de áudio real, o player deve:

- identificar a Megashop Santo Ângelo;
- ficar ONLINE;
- buscar a faixa piloto aprovada;
- exibir o título;
- ignorar a faixa com licença pendente;
- enviar heartbeat ao backend.

## Auditoria temporária

Acesse:

```text
http://localhost:8000/api/debug/status
```

Após iniciar o player, deve existir heartbeat para `megashop`.

## Lojas válidas

- panambi
- palmeira
- sao-borja
- tupancireta
- megashop
- mix

## Critério para avançar

Não avançar para deploy na VPS enquanto o teste local não passar para a Megashop.
