from abc import ABC, abstractmethod
import requests


class Platform(ABC):

    def __init__(self, name_vacancy):
        self.name_vacancy = name_vacancy

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(Platform):

    def get_vacancies(self):
        params = {
            'text': self.name_vacancy,
            'area': 1,  # Поиск по вакансиям города Москва
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице

        }
        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()
        req.close()
        return data


class SuperJobAPI(Platform):

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': 'v3.r.137642654.d35f7b9304e2a596a1ff8a7f85be229d0a98fa21'
                            '.3fee42b7294f5a27b80fca55203ce82ab5db2b3c'}

        params = {
            'keywords': self.name_vacancy,
            'town': 'Москва',  # Поиск по вакансиям города Москва
            'count': 100  # Кол-во вакансий на 1 странице

        }
        req = requests.get("https://api.superjob.ru/2.0/vacancies/", params, headers=headers)  # Посылаем запрос к API
        data = req.content.decode()
        req.close()
        return data
