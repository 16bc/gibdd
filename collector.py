"""
Получаем данные о ДТП с сайта гибдд.рф
"""

from bs4 import BeautifulSoup as bs
import requests
import json


def send_sms():
    # Phone number file workflow creating from secrets before package and deployment
    try:
        with open("./phone.sms", 'r') as file:
            phone_number = file.read(11)
            print("Phone number was read.")
        url = f"https://sms.ru/sms/send?api_id=3448D158-B7FC-24C2-DC45-155EDBFC4B7F&to={phone_number}&msg=Ошибка_GIBDD&json=1"
        return requests.get(url)
    except:
        print("Send SMS Error!!!")
        return 0


def read_file(filename="data.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        return [0]


def get_remote_data(url="https://гибдд.рф/"):
    """
    Парсит сайт и возвращает :
    """
    print("Получение данных с сайта...")
    try:
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        table = soup.find('table', {'class': "b-crash-stat"})

        head_str = str(table.th)  # Текст Заголовка
        data = [head_str[74:84]]  # Срезаем дату
        tags = table.find_all('td')  # достаём теги <td>
        tags = [tag.string for tag in tags]  # Извлекаем содержимое тегов
        # Just for fun:
        # data = {key: tags[tags.index(key)+1] for key in tags if (tags.index(key) % 2 == 0)}
        # Just for tests:
        # data = {tags[i]: tags[i + 1] for i in range(0, len(tags), 2)}
        nums = [tags[i] for i in range(1, 10, 2)]
        data.extend(nums)
        print(f"Получены данные с сайта {url} за {data[0]}:")
        print(data)
        return data
    except:
        print("Ошибка в полученных данных")
        send_sms()
        return 0


def readfile(path="./data.json"):
    try:
        with open(path, 'r') as file:
            last_string = file.readlines()[-1]  # [date, {stats}] or [0]
            try:
                return json.loads(last_string)
            except:
                return False
    except:
        print(f"Read file error! Check the file {path}")
        send_sms()
        exit(1)


def writefile(data, path="./data.json"):
    try:
        with open(path, 'a', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)  # ensure_ascii=False - Не заменять кириллицу на коды
            file.write('\n')
            return 0
    except:
        print(f"Write file error! Check the file {path}")
        send_sms()
        exit(1)


def collect():
    url = 'https://гибдд.рф/'
    # Читаем и десерим последнюю строку из файла
    last_list = readfile()

    # Получаем лист с данными с сайта
    new_datalist = get_remote_data(url)

    # Если дата из файла и дата с сайта отличаются, пишем в файл новую строку:
    if not last_list or (last_list[0] != new_datalist[0]):
        if writefile(new_datalist) == 0:
            return "Данные добавлены."
    else:
        return "Данные не обновлены."


if __name__ == '__main__':
    collect()
