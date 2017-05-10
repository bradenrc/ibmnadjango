from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from forms import CampingRecomendationForm
from models import Person, Demos
from .tables import PersonTable, DemosTable
from models import camping_results
import urllib3, requests, json
from django.db import connection
import app.apis

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)


    # demos = Demos.objects.all()
    # demos_table = DemosTable(demos)
    demos_table = DemosTable(Demos.objects.values("name", 'description', 'path'))

    #print demos_table.rows()[0]

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'demos': demos_table,
        }
    )

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
                #run prediction
                pred = app.apis.camping_predict_purchase(post.gender, post.age, m, j)

                #create new instance of camping_results entry
                cr = camping_results()
                cr.person = post #the form submited a new person, set the results fk to person
                cr.rawprediction = cr #store the returned blob

                #convert results to json to grab specific values
                crj = json.loads(pred)
                cr.product = crj["result"]["predictedLabel"]
                cr.prediction = crj["result"]["prediction"]
                cr.save()

            except Exception, e:
                print "error running prediction"
                print cr
                print e

            return redirect('/camping', pk=post.pk)
    else:
        form = CampingRecomendationForm()

    ptable = PersonTable(Person.objects.values('name', 'gender', 'marital', 'age', 'job',
                                               'camping_results__product', 'camping_results__prediction'))

    #grab the current list of predictions and the count of all predictions (for bound on chart)
    with connection.cursor() as cursor:
        sumres = cursor.execute("select count(*) as pcount, product from app_camping_results group by product").fetchall()
        tcount = cursor.execute("select count(*) from app_camping_results").fetchall()[0][0]

    #the chart wants very specific formating, easiest way is to convert to a list
    sumres_list = []
    for c, v in sumres:
         sumres_list.append([c, v.encode("utf-8")])


    print sumres_list
    print tcount

    return render(request, 'app/camping.html', {'title': 'Camping',
                                                'form': form,
                                                'people': ptable,
                                                'sumres': sumres_list,
                                                "tcount": tcount},
                  RequestContext(request, locals()))