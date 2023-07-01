from src.selection_of_vacancies import Data_recording, HH_vacancy, SJ_vacancy
from src.api_platforms import HeadHunterAPI, SuperJobAPI
import json


def input_user():
    json_obj_hh = json.loads(hh_api.get_vacancies())  # поиск вакансий по API
    json_obj_sj = json.loads(sj_api.get_vacancies())
    vacancy = []
    for i in json_obj_hh['items']:
        obj_v = HH_vacancy(i)
        data = obj_v.attribute_vacancy()
        vacancy.append(data)
    for i in json_obj_sj['objects']:
        obj_v = SJ_vacancy(i)
        data = obj_v.attribute_vacancy()
        vacancy.append(data)
    file_save = Data_recording(vacancy)
    file_save.recording()


def open_file_vacancies():
    with open('../files/vacancies.json', 'r', encoding='utf8') as file:
        f = json.load(file)
        for i in f:
            print(i['name'])


input_user_p = 'HH и SJ'
user = 'Python'
hh_api = HeadHunterAPI(user)
sj_api = SuperJobAPI(user)
input_user()
print('По Вашему запросу было собрано несколько вакансий, ознакомьтесь...')
open_file_vacancies()
