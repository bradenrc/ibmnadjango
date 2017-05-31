import urllib3, json
import random
import requests
import json

from app.models import ApiParameters, SuperHero


def camping_predict_purchase(gender, age, marital, job):
    """Watson API Prediction for Camping Equipment
    example params could be:
    # gender = "M"
    # age = 55
    # marital = "Single"
    # job = "Executive"
    """

    apip = ApiParameters.objects.filter(api_name='camping_predict_purchase')[0]
    id = apip.api_id  # "09171b0e-d473-4f0e-9d11-73bcd330ca67"
    version = apip.version  # "https://ibm-watson-ml.mybluemix.net/v2/artifacts/models/09171b0e-d473-4f0e-9d11-73bcd330ca67/versions/7e684513-a525-4510-90d5-a87ba6d22ab7"

    service_path = apip.service_path  # 'https://ibm-watson-ml.mybluemix.net'
    username = apip.username  # "35f91983-2730-4f14-8f4c-b821bf7c4c5a"
    password = apip.password  # "babcc6ca-c50e-414a-8cc3-535afb5f1fb8"

    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    url = '{}/v2/identity/token'.format(service_path)
    response = requests.get(url, headers=headers)
    mltoken = json.loads(response.text).get('token')

    header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
    scoring_href = apip.endpoint  # "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2080"

    age = int(age)
    payload_scoring = {"record": [gender, age, marital, job]}

    response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
    result = response_scoring.text
    return result


def score_super_hero(hero):
    sh = SuperHero.objects.get(heroid=hero)

    Hero = sh.heroid
    Efficienyv = sh.Efficienyv
    Mitigationv = sh.Mitigationv
    Suportv = sh.Suportv
    Ultimates = sh.Ultimates
    Scalingv = sh.Scalingv
    Productionv = sh.Productionv
    Depthv = sh.Depthv
    Funv = sh.Funv
    DE = sh.DE
    Fights = int(sh.Fights)

    url = "https://heroscore.mybluemix.net/score?Hero={}&Efficiencyv={}&Mitigationv={}&Supportv={}&Ultimatev={}&Scalingv={}&Productionv={}&Depthv={}&Funv={}&DEv={}&Fights={}".format(
        Hero,
        Efficienyv,
        Mitigationv,
        Suportv,
        Ultimates,
        Scalingv,
        Productionv,
        Depthv,
        Funv,
        DE,
        Fights
        )

    r = requests.get(url)
    r_json = json.loads(r.text)
    return  r_json["results"][0]["Score"]

# def super_hero_fight_prediction(hero):
#
#     heros = SuperHeroFight.heros
#     print heros[hero]
