There are three ways you can use this repository:

1. run the django site local:<Br>
-clone the repo<Br>
-in terminal go to site<Br>
-python -m pip install -r requirements.txt<Br>
-python manage.py runserver<Br>

2. Run Via the Docker Image posted to Docker:<Br>
docker pull ibmsparkna/django<Br>
docker run -p 8000:8000 ibmsparkna/django<Br>

3. Build your own docker image, for example<Br>
-clone repo<Br>
-run: docker build -t tag/name .<Br>
-run image: docker run -p 8000:8000 tag/name<Br>
