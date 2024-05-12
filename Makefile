include ./.env

build:
	docker build -t get-imoveis --no-cache .

run:
	docker run --env-file .env --network ${DEV_CONTAINER_NETWORK} -p ${APPLICATION_PORT}:8000 --name get-imoveis -d address-service
