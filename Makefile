start:
	docker-compose pull
	docker-compose build --no-cache
	docker-compose up -d
delete app:
	docker stop speech-assistant-analyzer_app_1
	docker rm speech-assistant-analyzer_app_1
	docker image rm speech-assistant-analyzer_app:latest
