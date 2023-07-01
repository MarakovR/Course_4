from abc import ABC, abstractmethod
import json


class Vacancy(ABC):
    """ Определяем атрибуты вакансий """

    def __init__(self, vacancy):
        self.vacancy = vacancy

    @abstractmethod
    def attribute_vacancy(self):
        pass


class HH_vacancy(Vacancy):

    def __init__(self, vacancy):
        super().__init__(vacancy)
        self.name_job = self.vacancy['name']
        self.url = f"https://hh.ru/vacancy/{self.vacancy['id']}"
        if self.vacancy['salary'] is None:
            self.salary = "Заработная плата не указана"
        elif self.vacancy['salary']['from'] is None:
            self.salary = f"Заработная плата до {self.vacancy['salary']['to']}"
        elif self.vacancy['salary']['to'] is None:
            self.salary = f"Заработная плата от {self.vacancy['salary']['from']}"
        else:
            self.salary = f"Средняя ЗП {(int(self.vacancy['salary']['from']) + int(self.vacancy['salary']['to'])) / 2}"
        if self.vacancy['snippet']['responsibility'] is None:
            self.specification = "Описание отсутствует"
        else:
            self.specification = self.vacancy['snippet']['responsibility']

    def attribute_vacancy(self):

        dict_vacancies = {"name": self.name_job, "url": self.url, "salary": self.salary,
                          "specification": self.specification}
        return dict_vacancies


class SJ_vacancy(Vacancy):

    def __init__(self, vacancy):
        super().__init__(vacancy)
        self.name_job = self.vacancy['profession']
        self.url = self.vacancy['link']
        if self.vacancy['payment_from'] is None and self.vacancy['payment_to'] is None:
            self.salary = "Заработная плата не указана"
        elif self.vacancy['payment_from'] is None:
            self.salary = f"Заработная плата до {self.vacancy['payment_to']}"
        elif self.vacancy['payment_to'] is None:
            self.salary = f"Заработная плата от {self.vacancy['payment_from']}"
        else:
            self.salary = f"Средняя ЗП {(int(self.vacancy['payment_from']) + int(self.vacancy['payment_to'])) / 2}"
        if self.vacancy['candidat'] is None:
            self.specification = "Описание отсутствует"
        else:
            self.specification = self.vacancy['candidat']

    def attribute_vacancy(self):

        dict_vacancies = {"name": self.name_job, "url": self.url, "salary": self.salary,
                          "specification": self.specification}
        return dict_vacancies


class Data_recording:
    """ Записываем вакансии в файл """

    def __init__(self, data):
        self.data = data

    def recording(self):
        f = open('../files/vacancies.json', mode='w', encoding='utf8')
        f.write(json.dumps(self.data, ensure_ascii=False))
        f.close()
