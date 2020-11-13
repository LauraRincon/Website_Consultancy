build:
	sudo docker build --tag web_consultancy:latest .
run:
	sudo docker run -ti -p 8000:8000 web_consultancy:latest bash
runserver:
		python3 ./manage.py runserver 0.0.0.0:8000
