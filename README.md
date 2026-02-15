# Libguard

O Libguard é uma plataforma para detectar se há alguma vulnerabilidade e se há dependências incompatíveis no projeto.

## Como rodar

> Certifique-se de possuir o Docker e o Docker Compose instalados em sua máquina

### Clone o projeto

`git clone https://github.com/Libguard/libguard-backend.git`

### Entre no projeto

`cd libguard`

### Execute com

`docker compose up -d --build`

Acesse [localhost:8000](http://127.0.0.1:8000) no seu navegador favorito

### Ver logs

`docker compose logs -f api`

### Rodar migrations (apenas se alterar algum models.py)

```
docker compose exec api bash # ou docker compose exec api sh

# Dentro do container execute:
uv run python3 manage.py makemigrations
```

ou

`docker compose exec api uv run python3 manage.py makemigrations`

### Parar o projeto

`docker compose down`

ou

`docker compose down -v # Para remover os volumes, incluindo o banco de dados SQLite3`