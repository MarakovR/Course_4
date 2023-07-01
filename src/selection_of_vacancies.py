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


class User_vacancies(ABC):
    """ Сохраняет содержимое объектов отобранных вакансий в файл """

    def __init__(self, api_plat):
        self.api_plat = api_plat

    @abstractmethod
    def save_user_vacancy(self):
        pass


class HH_user_vacancies(User_vacancies):

    def save_user_vacancy(self):
        json_obj = json.loads(self.api_plat.get_vacancies())
        vacancy = []
        for i in json_obj['items']:
            obj_vacancy = HH_vacancy(i)
            data = obj_vacancy.attribute_vacancy()
            vacancy.append(data)
        recording_hh(vacancy)


class SJ_user_vacancies(User_vacancies):

    def save_user_vacancy(self):
        json_obj = json.loads(self.api_plat.get_vacancies())
        vacancy = []
        for i in json_obj['objects']:
            obj_vacancy = SJ_vacancy(i)
            data = obj_vacancy.attribute_vacancy()
            vacancy.append(data)
        recording_sj(vacancy)


class Output_user:
    """ Преобразует вывод информации по вакансиям пользователю """

    def __init__(self, top):
        self.vacancies_sj = None
        self.vacancies_hh = None
        self.top = top

    def output_hh(self):
        self.vacancies_hh = open_file_vacancies_hh()
        top_vacancies = sorted(self.vacancies_hh, key=lambda d: d['salary'], reverse=True)
        for i in top_vacancies[0:int(self.top)]:
            print(f"Наименование вакансии - {i['name']}")
            print(f"Заработная плата - {i['salary']}, уточнить по ссылке ниже")
            print(f"Описание - {i['specification']}")
            print(f"Ссылка - {i['url']}")
            print()
            print("******************************")
            print()

    def output_sj(self):
        self.vacancies_sj = open_file_vacancies_sj()
        top_vacancies = sorted(self.vacancies_sj, key=lambda d: d['salary'], reverse=True)
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


def recording_hh(data):  # записывает данные в файл vacancies_hh.json
    f = open('../files/vacancies_hh.json', mode='w', encoding='utf8')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()


def recording_sj(data):  # записывает данные в файл vacancies_sj.json
    f = open('../files/vacancies_sj.json', mode='w', encoding='utf8')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()


def open_file_vacancies_hh():  # возвращает данные из файла vacancies_hh.json
    with open('../files/vacancies_hh.json', 'r', encoding='utf8') as file:
        f = json.load(file)
        return f


def open_file_vacancies_sj():  # возвращает данные из файла vacancies_sj.json
    with open('../files/vacancies_sj.json', 'r', encoding='utf8') as file:
        f = json.load(file)
        return f
