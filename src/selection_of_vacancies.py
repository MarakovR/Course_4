from abc import ABC, abstractmethod
import json


class Vacancy(ABC):
    """ Определяет атрибуты вакансий """

    def __init__(self, vacancy):
        self.vacancy = vacancy

    @abstractmethod
    def attribute_vacancy(self):
        pass


class HH_vacancy(Vacancy):
    """ Определяет необходимые атрибуты вакансий c hh.ru """

    def __init__(self, vacancy):
        super().__init__(vacancy)
        self.name_job = self.vacancy['name']
        self.url = f"https://hh.ru/vacancy/{self.vacancy['id']}"
        if self.vacancy['salary'] is None:
            self.salary = 0
        elif self.vacancy['salary']['from'] is None:
            self.salary = int(self.vacancy['salary']['to'])
        elif self.vacancy['salary']['to'] is None:
            self.salary = int(self.vacancy['salary']['from'])
        else:
            self.salary = (int(self.vacancy['salary']['from']) + int(self.vacancy['salary']['to'])) / 2
        if self.vacancy['snippet']['responsibility'] is None:
            self.specification = "Описание отсутствует"
        else:
            self.specification = self.vacancy['snippet']['responsibility']

    def attribute_vacancy(self):

        dict_vacancies = {"name": self.name_job, "url": self.url, "salary": self.salary,
                          "specification": self.specification}
        return dict_vacancies


class SJ_vacancy(Vacancy):
    """ Определяет необходимые атрибуты вакансий c superjob.ru """

    def __init__(self, vacancy):
        super().__init__(vacancy)
        self.name_job = self.vacancy['profession']
        self.url = self.vacancy['link']
        if self.vacancy['payment_from'] is None and self.vacancy['payment_to'] is None:
            self.salary = 0
        elif self.vacancy['payment_from'] is None:
            self.salary = int(self.vacancy['payment_to'])
        elif self.vacancy['payment_to'] is None:
            self.salary = int(self.vacancy['payment_from'])
        else:
            self.salary = (int(self.vacancy['payment_from']) + int(self.vacancy['payment_to'])) / 2
        if self.vacancy['candidat'] is None:
            self.specification = "Описание отсутствует"
        else:
            self.specification = self.vacancy['candidat']

    def attribute_vacancy(self):

        dict_vacancies = {"name": self.name_job, "url": self.url, "salary": self.salary,
                          "specification": self.specification}
        return dict_vacancies


class User_vacancies:
    """ Сохраняет содержимое объектов отобранных вакансий в файл """
    vacancies = {}

    def __init__(self, api_hh, api_sj):
        self.api_hh = api_hh
        self.api_sj = api_sj

    def save_user_vacancy(self):
        json_obj_hh = json.loads(self.api_hh.get_vacancies())
        json_obj_sj = json.loads(self.api_sj.get_vacancies())
        list_data_hh = []
        list_data_sj = []
        for vac in json_obj_hh['items']:
            obj_vacancy = HH_vacancy(vac)
            data_hh = obj_vacancy.attribute_vacancy()
            list_data_hh.append(data_hh)
        for vac in json_obj_sj['objects']:
            obj_vacancy = SJ_vacancy(vac)
            data_sj = obj_vacancy.attribute_vacancy()
            list_data_sj.append(data_sj)
        User_vacancies.vacancies['hh'] = list_data_hh
        User_vacancies.vacancies['sj'] = list_data_sj


class Output_user:
    """ Преобразует вывод информации по вакансиям пользователю """

    def __init__(self, landing, top=100):
        self.vacancies = None
        self.top = top
        self.landing = landing

    def output(self):
        self.vacancies = open_file_vacancies()[self.landing]
        top_vacancies = sorted(self.vacancies, key=lambda d: d['salary'], reverse=True)
        for i in top_vacancies[0:int(self.top)]:
            print(f"Наименование вакансии - {i['name']}")
            if i['salary'] == 0:
                print("Заработная плата - По договоренности")
            else:
                print(f"Заработная плата - {i['salary']} Уточнить по ссылке ниже")
            print(f"Описание - {i['specification']}")
            print(f"Ссылка - {i['url']}")
            print()
            print("******************************")
            print()


def recording(data):  # записывает данные в файл vacancies_hh.json
    f = open('../files/vacancies.json', mode='w', encoding='utf8')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()


def open_file_vacancies():  # возвращает данные из файла vacancies_hh.json
    with open('../files/vacancies.json', 'r', encoding='utf8') as file:
        f = json.load(file)
        return f
