# Venv
alias venv="source project_cemphris_venv/bin/activate"
# Docker
alias drundb="docker run --name postgresdb -p 5432:5432 -d -e POSTGRES_DB=project_cemphris -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=qweasd123 postgres:15.7"
alias drunredis="docker run --name redisdb -p 6379:6379 -d redis:7-alpine"
alias dbuildapp="docker build -t ayushmodi/project-cemphris:v0 ."
alias drmi="docker image remove"
alias dapp="docker compose exec -it pc_app bash"
alias dpush="docker push ayushmodi/project-cemphris:v0"
alias dpull="docker pull ayushmodi/project-cemphris:v0"
# Server
alias rsa="gunicorn --bind 0.0.0.0:8000 project_cemphris.asgi:application -k uvicorn.workers.UvicornWorker"
alias pmrs="python manage.py runserver"
# Django Db
alias pmmm="python manage.py makemigrations"
alias pmmg="python manage.py migrate"
alias pmds="python manage.py dbshell"
# Make ER
alias pmgm="python manage.py graph_models -a > erd.dot"
# Git
alias ga="git add"
alias gcm="git commit -m"
alias gp="git push"
alias gc="git checkout"
# psql
# alias pslh= "psql -U postgres -h localhost -p 5432"
# Firewall
alias fwe="sudo ufw enable"
alias fwd="sudo ufw disable"