# Arquitetura inicial

## Componentes

- `apps/player`: player das lojas;
- `apps/admin`: painel administrativo;
- `server`: API, programação, autenticação e logs;
- `storage/music`: arquivos de música (não versionados no Git por padrão);
- `storage/campaigns`: áudios de campanha;
- `storage/licenses`: evidências e documentos de licença;
- `scripts`: implantação, importação e manutenção.

## Princípio de implantação

Aplicação web hospedada na VPS e acessada por HTTPS. Cada loja terá identidade própria e receberá sua grade centralmente.
