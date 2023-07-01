from src.api_platforms import HeadHunterAPI, SuperJobAPI
from src.selection_of_vacancies import HH_user_vacancies, open_file_vacancies_hh, SJ_user_vacancies, Output_user, \
    open_file_vacancies_sj

user_vacancy = (input('Какая вакансия Вас интересует?\n'))
platforms_input = (input('На какой площадке вы хотите осуществить поиск? HH (HeadHunter), SJ (SuperJob)\n').lower())
if platforms_input == 'HH'.lower():
    api = HeadHunterAPI(user_vacancy)
    obj_user_vac = HH_user_vacancies(api)
    obj_user_vac.save_user_vacancy()
    if not open_file_vacancies_hh():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output = Output_user(100)
            obj_output.output_hh()
        elif user_answer == "ТОП".lower():
            obj_output = Output_user(input('Введите количество ТОП\n'))
            obj_output.output_hh()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')
elif platforms_input == 'SJ'.lower():
    api = SuperJobAPI(user_vacancy)
    obj_user_vac = SJ_user_vacancies(api)
    obj_user_vac.save_user_vacancy()
    if not open_file_vacancies_sj():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output = Output_user(100)
            obj_output.output_sj()
        elif user_answer == "ТОП".lower():
            obj_output = Output_user(input('Введите количество ТОП\n'))
            obj_output.output_sj()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')
elif platforms_input == 'HH, SJ'.lower() or 'ВСЕ'.lower():
    api_hh = HeadHunterAPI(user_vacancy)
    api_sj = SuperJobAPI(user_vacancy)
    obj_user_vac_hh = HH_user_vacancies(api_hh)
    obj_user_vac_sj = SJ_user_vacancies(api_sj)
    obj_user_vac_hh.save_user_vacancy()
    obj_user_vac_sj.save_user_vacancy()
    if not open_file_vacancies_hh():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output = Output_user(100)
            obj_output.output_hh()
            obj_output.output_sj()
        elif user_answer == "ТОП".lower():
            obj_output = Output_user(input('Введите количество ТОП\n'))
            obj_output.output_hh()
            obj_output.output_sj()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')
