from api_platforms import HeadHunterAPI, SuperJobAPI
from selection_of_vacancies import User_vacancies, Output_user, recording, open_file_vacancies

""" Работа с пользователем """
user_vacancy = (input('Какая вакансия Вас интересует?\n'))

api = [HeadHunterAPI(user_vacancy), SuperJobAPI(user_vacancy)]
user_vac = User_vacancies(api[0], api[1])
user_vac.save_user_vacancy()
recording(user_vac.vacancies)

platforms_input = (input('На какой площадке вы хотите осуществить поиск? HH (HeadHunter), SJ (SuperJob)\n').lower())
if platforms_input == 'HH'.lower():
    if not open_file_vacancies():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output = Output_user('hh')
            obj_output.output()
        elif user_answer == "ТОП".lower():
            obj_output = Output_user('hh', input('Введите количество ТОП\n'))
            obj_output.output()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')

elif platforms_input == 'SJ'.lower():
    if not open_file_vacancies():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output = Output_user('sj')
            obj_output.output()
        elif user_answer == "ТОП".lower():
            obj_output = Output_user('sj', input('Введите количество ТОП\n'))
            obj_output.output()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')

elif platforms_input == 'HH, SJ'.lower() or 'ВСЕ'.lower():
    if not open_file_vacancies():
        print('Запрошенных вакансий найти не удалось')
    else:
        user_answer = input(
            'Интересующие Вас вакансии собраны, хотите просмотреть их все или сформировать топ? (введите "ВСЕ" или '
            '"ТОП")\n').lower()
        if user_answer == "ВСЕ".lower():
            obj_output_hh = Output_user('hh')
            obj_output_sj = Output_user('sj')
            obj_output_hh.output()
            obj_output_sj.output()
        elif user_answer == "ТОП".lower():
            num_top = input('Введите количество ТОП\n')
            obj_output_hh = Output_user('hh', num_top)
            obj_output_sj = Output_user('sj', num_top)
            print(f'ТОП {num_top} площадки HH.ru:')
            obj_output_hh.output()
            print(f'ТОП {num_top} площадки SuperJob.ru:')
            obj_output_sj.output()
        else:
            print('Нет такого варианта ответа, попробуйте сначала')
