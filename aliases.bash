# Venv
alias venv="source project_cemphris_venv/bin/activate"
# Docker
alias rundb="docker run --name postgresdb -p 5432:5432 -d -e POSTGRES_DB=project_cemphris -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=qweasd123 postgres:15.7"
alias runredis="docker run --name redisdb -p 6379:6379 -d redis:7-alpine"
# Server
alias rsa="gunicorn --bind 0.0.0.0:8000 project_cemphris.asgi:application -k uvicorn.workers.UvicornWorker"
alias pmrs="python manage.py runserver"
# Django Db
alias pmmm="python manage.py makemigrations"
alias pmmg="python manage.py migrate"
alias pmds="python manage.py dbshell"
