import urllib3, json
import random
import requests
import json

from app.models import ApiParameters, SuperHero
import math
import decimal


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


# def score_super_hero(hero):
#     sh = SuperHero.objects.get(heroid=hero)
#
#     Hero = sh.heroid
#     Efficienyv = sh.Efficienyv
#     Mitigationv = sh.Mitigationv
#     Suportv = sh.Suportv
#     Ultimates = sh.Ultimates
#     Scalingv = sh.Scalingv
#     Productionv = sh.Productionv
#     Depthv = sh.Depthv
#     Funv = sh.Funv
#     DE = sh.DE
#     Fights = int(sh.Fights)
#
#     url = "https://heroscore.mybluemix.net/score?Hero={}&Efficiencyv={}&Mitigationv={}&Supportv={}&Ultimatev={}&Scalingv={}&Productionv={}&Depthv={}&Funv={}&DEv={}&Fights={}".format(
#         Hero,
#         Efficienyv,
#         Mitigationv,
#         Suportv,
#         Ultimates,
#         Scalingv,
#         Productionv,
#         Depthv,
#         Funv,
#         DE,
#         Fights
#         )
#
#     r = requests.get(url)
#     r_json = json.loads(r.text)
#     return  r_json["results"][0]["Score"]

def score_super_hero(hero, observers, home, night, duration):
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
    role = sh.Role


    cos = observers
    duration_val = duration

    if home:
        ht = 1
    else:
        ht = 0

    if night:
        dtfight = 0
    else:
        dtfight = 1

    eb = 1



    form_citizen_observers = decimal.Decimal(-0.0000001826)
    form_duration = decimal.Decimal(0.002169)
    form_home_turf = decimal.Decimal(-0.2956)
    form_hero_villian = decimal.Decimal(-1.098)
    form_daytime_fight = decimal.Decimal(-0.1871)
    form_extended_battle = decimal.Decimal(0.5708)

    form_Efficienyv = decimal.Decimal(15.83)
    form_Mitigationv = decimal.Decimal(-16.77)
    form_Suportv = decimal.Decimal(15.1)
    form_Ultimates = decimal.Decimal(-50.83)
    form_Scalingv = decimal.Decimal(40.33)
    form_Productionv = decimal.Decimal(-10.09)
    form_Depthv = decimal.Decimal(3.08)
    form_Funv = decimal.Decimal(-6.668)
    form_DE = decimal.Decimal(4.269)
    form_Fights = decimal.Decimal(-18.11)

    # Role:
    role_d = {
        "Bruiser": decimal.Decimal(-143.6),
        "Controller": decimal.Decimal(-70),
        "Destroyer": decimal.Decimal(-90.05),
        "Dominator": decimal.Decimal(-220.9),
        "Doominator": decimal.Decimal(-196.4),
        "Fighter": decimal.Decimal(-215.6),
        "Leader": decimal.Decimal(-199.9),
        "Nuker": decimal.Decimal(-281.5),
        "Saboteur": decimal.Decimal(-166.3),
        "Skirmisher": decimal.Decimal(-170.2),
        "Summoner": decimal.Decimal(-204.4)
    }

    exps_v1 = (form_citizen_observers * cos) + (form_duration * duration_val) + (form_home_turf * ht) + \
              (form_daytime_fight * dtfight) + (form_extended_battle * eb) + (form_Efficienyv * Efficienyv) + \
              (form_Mitigationv * Mitigationv) + (form_Suportv * Suportv) + (form_Ultimates * Ultimates)  + \
              (form_Scalingv * Scalingv) + (form_Productionv * Productionv) + (form_Depthv * Depthv)  + \
              (form_Funv * Funv) + (form_DE * DE) + (form_Fights * Fights) + (role_d[role]) + decimal.Decimal(720.1)

    score = math.exp(exps_v1) / (1 + math.exp(exps_v1))
    return score
