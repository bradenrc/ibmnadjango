from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from forms import CampingRecomendationForm
from django.forms import modelformset_factory
from models import Person
from .tables import PersonTable
from models import camping_results
import urllib3, requests, json, os

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def predict_purchase(gender, age, marital, job):
    id = "09171b0e-d473-4f0e-9d11-73bcd330ca67"
    version = "https://ibm-watson-ml.mybluemix.net/v2/artifacts/models/09171b0e-d473-4f0e-9d11-73bcd330ca67/versions/7e684513-a525-4510-90d5-a87ba6d22ab7"

    service_path = 'https://ibm-watson-ml.mybluemix.net'
    username = "35f91983-2730-4f14-8f4c-b821bf7c4c5a"
    password = "babcc6ca-c50e-414a-8cc3-535afb5f1fb8"

    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    url = '{}/v2/identity/token'.format(service_path)
    response = requests.get(url, headers=headers)
    mltoken = json.loads(response.text).get('token')

    header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
    scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2080"

    # gender = "M"
    # age = 55
    # marital = "Single"
    # job = "Executive"

    age = int(age)
    payload_scoring = {"record":[gender, age, marital, job]}

    response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
    result = response_scoring.text
    return result


#
# class camping_results(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     rawprediction = models.CharField(max_length=2000)
#     product = models.CharField(max_length=30)
#     prediction = models.FloatField()


from models import Person

p = Person.objects.get(id=1)


def camping(request):
    if request.method == "POST":
        form = CampingRecomendationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            for k, v in Person.marital_c:
                if k == post.marital: m = v

            for k, v in Person.job_c:
                if k == post.job: j = v

            try:
                pred = predict_purchase(post.gender, post.age, m, j)
                cr = camping_results()
                crj = json.loads(pred)
                cr.person = post
                cr.product = crj["result"]["predictedLabel"]
                cr.rawprediction = cr
                cr.prediction = crj["result"]["prediction"]
                cr.save()
            except Exception, e:
                print "error running prediction"
                print cr
                print e

            return redirect('./app/camping.html', pk=post.pk)
    else:
        form = CampingRecomendationForm()

    ptable = PersonTable(Person.objects.all())

    sumres = [[10, 'test'], [10, 'test2'], [10, 'test3']]
    tcount = 30

    return render(request, 'app/camping.html', {'form': form, 'people': ptable, 'sumres': sumres, "tcount": tcount},
                  RequestContext(request, locals()))