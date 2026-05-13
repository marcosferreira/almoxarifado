SHELL := /bin/bash

COMPOSE_FILE ?= docker-compose.dev.yml
DC := docker compose -f $(COMPOSE_FILE)
APP_SERVICE ?= app
DB_SERVICE ?= db
ARGS ?=
CMD ?= bash

.DEFAULT_GOAL := help

.PHONY: help \
	up up-d down down-v down-orphans \
	build build-nc rebuild pull \
	start stop restart ps config images top events \
	logs logs-f logs-app logs-db \
	exec-app exec-db run-app \
	bash-app bash-db \
	migrate makemigrations createsuperuser collectstatic test dbshell \
	kill rm-stopped pause unpause

help: ## Mostra esta ajuda
	@echo "Comandos Make para ambiente de desenvolvimento (docker-compose.dev.yml):"
	@awk 'BEGIN {FS = ":.*## "; printf "\nUso:\n  make <alvo>\n\nAlvos:\n"} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Sobe os servicos em foreground
	$(DC) up

up-d: ## Sobe os servicos em background
	$(DC) up -d

down: ## Para e remove os containers/rede
	$(DC) down

down-v: ## Para e remove containers/rede/volumes
	$(DC) down -v

down-orphans: ## Remove containers orfaos
	$(DC) down --remove-orphans

build: ## Faz build das imagens
	$(DC) build

build-nc: ## Faz build sem cache
	$(DC) build --no-cache

rebuild: ## Reconstroi e sobe em background
	$(DC) up -d --build

pull: ## Faz pull das imagens
	$(DC) pull

start: ## Inicia containers existentes
	$(DC) start

stop: ## Para os servicos
	$(DC) stop

restart: ## Reinicia os servicos
	$(DC) restart

ps: ## Lista status dos containers
	$(DC) ps

config: ## Exibe configuracao resolvida do compose
	$(DC) config

images: ## Lista imagens usadas pelos servicos
	$(DC) images

top: ## Exibe processos em execucao nos containers
	$(DC) top

events: ## Exibe eventos em tempo real
	$(DC) events

logs: ## Exibe logs de todos os servicos
	$(DC) logs

logs-f: ## Exibe logs seguindo em tempo real
	$(DC) logs -f

logs-app: ## Exibe logs do servico app
	$(DC) logs -f $(APP_SERVICE)

logs-db: ## Exibe logs do servico db
	$(DC) logs -f $(DB_SERVICE)

exec-app: ## Executa comando no app (uso: make exec-app CMD='python manage.py check')
	$(DC) exec $(APP_SERVICE) $(CMD)

exec-db: ## Executa comando no db (uso: make exec-db CMD='psql -U postgres -d almoxarifado')
	$(DC) exec $(DB_SERVICE) $(CMD)

run-app: ## Roda comando one-off no app (uso: make run-app CMD='python manage.py shell')
	$(DC) run --rm $(APP_SERVICE) $(CMD)

bash-app: ## Abre shell bash no container app
	$(DC) exec $(APP_SERVICE) bash

bash-db: ## Abre shell bash no container db
	$(DC) exec $(DB_SERVICE) bash

migrate: ## Executa migracoes do Django
	$(DC) exec $(APP_SERVICE) python manage.py migrate

makemigrations: ## Cria novas migracoes do Django
	$(DC) exec $(APP_SERVICE) python manage.py makemigrations $(ARGS)

createsuperuser: ## Cria superusuario no Django
	$(DC) exec $(APP_SERVICE) python manage.py createsuperuser

collectstatic: ## Coleta arquivos estaticos
	$(DC) exec $(APP_SERVICE) python manage.py collectstatic --noinput

test: ## Roda os testes Django
	$(DC) exec $(APP_SERVICE) python manage.py test $(ARGS)

dbshell: ## Abre shell do banco via Django
	$(DC) exec $(APP_SERVICE) python manage.py dbshell

kill: ## Envia sinal para containers (uso: make kill ARGS='-s SIGKILL')
	$(DC) kill $(ARGS)

rm-stopped: ## Remove containers parados dos servicos
	$(DC) rm -f

pause: ## Pausa os servicos
	$(DC) pause

unpause: ## Despausa os servicos
	$(DC) unpause
