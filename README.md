There are three ways you can use this repository:

1. run the django site local:<Br>
-clone the repo<Br>
-in terminal go to /demo<Br>
-python -m pip install -r requirements.txt<Br>
-python manage.py runserver<Br>

2. Run Via the Docker Image posted to Docker:<Br>
docker pull ibmsparkna/django<Br>
docker run -p 8000:8000 ibmsparkna/django<Br>

3. Build your own docker image, for example<Br>
-clone repo<Br>
-run: docker build -t tag/name .<Br>
-run image: docker run -p 8000:8000 tag/name<Br>


4. Bluemix - After Creating your Python Service:
bx login (select the proper org, area, etc.)
bx app push django_demo  -c "sh run.sh" (replace django_demo with your Bluemix app name)

