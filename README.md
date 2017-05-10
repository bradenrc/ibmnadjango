There are three ways you can use this repository:

1. run the django site local:
-clone the repo
-in terminal go to site
-python -m pip install -r requirements
-python manage.py runserver

2. Run Via the Docker Image posted to Docker:
docker pull ibmsparkna/django
docker run ibmsparkna/django

3. Build your own docker image, for example
-clone repo
-run: docker build -t tag/name .
-run image: docker run tag/name
