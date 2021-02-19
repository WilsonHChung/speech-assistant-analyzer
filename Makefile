start:
	docker-compose build --no-cache
	docker run -p 5000:5000 -t -i --name speech-assistant-analyzer_app speech-assistant-analyzer_app:latest
delete:
	docker rm speech-assistant-analyzer_app
	docker image rm speech-assistant-analyzer_app:latest