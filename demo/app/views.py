from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from forms import CampingRecomendationForm, SubmitForm, SuperHeroFightForm, SuperHeroFightFormEH
from models import Person, Demos, SuperHeroFight
from .tables import PersonTable, DemosTable, SuperHeroTable
from models import camping_results
import urllib3, requests, json
from django.db import connection
import app.apis
import subprocess
from django_tables2 import RequestConfig


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    # demos = Demos.objects.all()
    # demos_table = DemosTable(demos)
    demos_table = DemosTable(Demos.objects.values("name", 'description', 'path'))

    # print demos_table.rows()[0]

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
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
                # run prediction
                pred = app.apis.camping_predict_purchase(post.gender, post.age, m, j)

                # create new instance of camping_results entry
                cr = camping_results()
                cr.person = post  # the form submited a new person, set the results fk to person
                cr.rawprediction = cr  # store the returned blob

                # convert results to json to grab specific values
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

    # grab the current list of predictions and the count of all predictions (for bound on chart)
    with connection.cursor() as cursor:
        sumres = cursor.execute(
            "select count(*) as pcount, product from app_camping_results group by product").fetchall()
        tcount = cursor.execute("select count(*) from app_camping_results").fetchall()[0][0]

    # the chart wants very specific formating, easiest way is to convert to a list
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


def streaming_intro(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    clicked = "Not Submitted"

    if request.method == "POST":
        form = SubmitForm(request.POST)
        if form.is_valid():
            clicked = "Submitted"
            # post = form.save(commit=False)
            print clicked

            r = subprocess.call("python ./app/util/load_random.py", shell=True)
            print r

            # return redirect('/streaming_intro')

    return render(
        request,
        'app/streaming_intro.html',
        {
            'title': 'Streaming',
            'clicked': clicked,
            'form': SubmitForm

        }
    )


def superhero(request):
    if request.method == "POST":
        form = SuperHeroFightForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            post.heroone_score = app.apis.score_super_hero(post.SuperHeroOne)
            post.herotwo_score = app.apis.score_super_hero(post.SuperHeroTwo)
            post.save()

            return redirect('/superhero', pk=post.pk)
    else:
        form = SuperHeroFightForm()

    fights = SuperHeroTable(SuperHeroFight.objects.order_by('-id'))
    RequestConfig(request).configure(fights)

    query = """SELECT
                  (sum(win) * 1.0) /  count(*) as winratio,
                  1 - ((sum(win) * 1.0) /  count(*)) as lossratio,
                  sh
                from
                  (
                SELECT
                  SuperHeroOne as sh,
                  CASE
                    WHEN heroone_score > herotwo_score THEN 1
                    ELSE 0
                  END AS WIN
                FROM
                  app_superherofight

                UNION ALL

                SELECT
                  SuperHeroTwo as sh,
                  CASE
                    WHEN heroone_score < herotwo_score THEN 1
                    ELSE 0
                  END AS WIN
                FROM
                  app_superherofight) t
                group by sh
                """

    # grab the current list of predictions and the count of all predictions (for bound on chart)
    with connection.cursor() as cursor:
        sumres = cursor.execute(query).fetchall()

    # the chart wants very specific formating, easiest way is to convert to a list
    sumres_list = []
    heros = []



    for wr, lr, sh in sumres:
        hname = str(SuperHeroFight.heroes[sh][1]).encode("utf-8")

        heros.append(hname)
        sumres_list.append([hname, lr, 'Loss'])
        sumres_list.append([hname, wr, 'Win'])



    #[['Hero1', 0.7, 'Loss'], ['Hero1', 0.3, 'Win'], ['Hero2', 0.75, 'Loss'],  ['Hero2', 0.25, 'Win'], ['Hero3', 0.9, 'Loss'], ['Hero3', 0.1, 'Win']]

    print heros
    print sumres_list

    return render(request, 'app/superhero.html', {'title': 'Superhero Fight!!',
                                                  'form': form,
                                                  'fights': fights,
                                                  'sumres_list': sumres_list,
                                                  'heros' : heros,
                                                  },
                  RequestContext(request, locals()))



def superheroeh(request):
    if request.method == "POST":
        form = SuperHeroFightFormEH(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            print "Home: ", home
            print "Duration: ", post.duration
            print "Night: ", post.night

            post.SuperHeroOne = 38

            post.heroone_score = app.apis.score_super_hero(38, post.observers, post.home, post.night, post.duration)
            post.herotwo_score = app.apis.score_super_hero(post.SuperHeroTwo, post.observers, post.home, post.night, post.duration)
            post.save()

            return redirect('/superheroeh', pk=post.pk)
    else:
        form = SuperHeroFightFormEH()

    fights = SuperHeroTable(SuperHeroFight.objects.all())

    query = """SELECT
                  (sum(win) * 1.0) /  count(*) as winratio,
                  1 - ((sum(win) * 1.0) /  count(*)) as lossratio,
                  sh
                from
                  (
                SELECT
                  SuperHeroOne as sh,
                  CASE
                    WHEN heroone_score > herotwo_score THEN 1
                    ELSE 0
                  END AS WIN
                FROM
                  app_superherofight

                UNION ALL

                SELECT
                  SuperHeroTwo as sh,
                  CASE
                    WHEN heroone_score < herotwo_score THEN 1
                    ELSE 0
                  END AS WIN
                FROM
                  app_superherofight) t
                group by sh
                """

    # grab the current list of predictions and the count of all predictions (for bound on chart)
    with connection.cursor() as cursor:
        sumres = cursor.execute(query).fetchall()

    # the chart wants very specific formating, easiest way is to convert to a list
    sumres_list = []
    heros = []



    for wr, lr, sh in sumres:
        hname = str(SuperHeroFight.heroes[sh][1]).encode("utf-8")

        heros.append(hname)
        sumres_list.append([hname, lr, 'Loss'])
        sumres_list.append([hname, wr, 'Win'])



    #[['Hero1', 0.7, 'Loss'], ['Hero1', 0.3, 'Win'], ['Hero2', 0.75, 'Loss'],  ['Hero2', 0.25, 'Win'], ['Hero3', 0.9, 'Loss'], ['Hero3', 0.1, 'Win']]

    print heros
    print sumres_list

    return render(request, 'app/superhero_eh.html', {'title': 'Superhero Fight!!',
                                                  'form': form,
                                                  'fights': fights,
                                                  'sumres_list': sumres_list,
                                                  'heros' : heros,
                                                  },
                  RequestContext(request, locals()))
