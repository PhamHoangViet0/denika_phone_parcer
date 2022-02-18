import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = 'https://denika.ua/c/mobilnie-i-aksessuari/mobilnie-telefoni'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.82 '
                  'Safari/537.36'
}


def get_html(url, headers):
    result = requests.get(url=url, headers=headers)
    if result:
        return result.text
    return f'Bad request. Сode {result.status_code}'


def get_info(url, headers, page_count):
    items = []

    html = get_html(url, headers)

    counter = 0
    while counter != page_count:
        counter += 1

        soup = BeautifulSoup(html, 'html.parser')
        blocks = soup.find_all('div', class_='product-box')

        for block in blocks:
            name = block.find('a', class_='product-title').get_text()
            code = int(block.find('span', class_='product-code').get_text()[5:])
            link = block.find('a', class_='product-title').get('href')
            price = int(''.join([i for i in block.find('span', class_='price').get_text() if i.isdigit()]))

            soup_from_phone = BeautifulSoup(get_html(link, headers), 'html.parser')
            brand_tag = soup_from_phone.find('span', class_='cell', string='Бренд')
            if brand_tag is None:
                brand = None
            else:
                brand = brand_tag.nextSibling.nextSibling.find('a').get_text()

            series_tag = soup_from_phone.find('span', class_='cell', string='Серия')
            if series_tag is None:
                series = None
            else:
                series = series_tag.nextSibling.nextSibling.find('a').get_text()

            os_tag = soup_from_phone.find('span', class_='cell', string='Операционная система')
            if os_tag is None:
                os = None
            else:
                os = os_tag.nextSibling.nextSibling.find('a').get_text()

            diagonal_tag = soup_from_phone.find('span', class_='cell', string='Диагональ дисплея, дюйм')
            if diagonal_tag is None:
                diagonal = None
            else:
                diagonal = diagonal_tag.nextSibling.nextSibling.get_text()

            resolution_tag = soup_from_phone.find('span', class_='cell', string='Разрешение дисплея')
            if resolution_tag is None:
                resolution = None
            else:
                resolution = resolution_tag.nextSibling.nextSibling.get_text()

            cpu_model_tag = soup_from_phone.find('span', class_='cell', string='Модель процессора')
            if cpu_model_tag is None:
                cpu_model = None
            else:
                cpu_model = cpu_model_tag.nextSibling.nextSibling.get_text()

            cpu_cores_tag = soup_from_phone.find('span', class_='cell', string='Количество ядер')
            if cpu_cores_tag is None:
                cpu_cores = None
            else:
                cpu_cores = cpu_cores_tag.nextSibling.nextSibling.find('a').get_text()

            # .nextSibling.find('a').get_text()
            # print(brand, '\n-------------------------\n')
            # if len(items) == 0:
            #     print(soup_from_phone)
            info = {
                'name': name,
                'code': code,
                'link': link,
                'price': price,
                'generic': {
                    'brand': brand,
                    'series': series,
                    'os': os},
                'display': {
                    'diagonal': diagonal,
                    'resolution': resolution
                },
                'cpu': {
                    'model': cpu_model,
                    'cores': cpu_cores
                }
            }
            items.append(info)
            print(len(items))
            print(info)

        next_page_tag = soup.find('a', string='>')
        if next_page_tag is None:
            break
        html = get_html(next_page_tag.get('href'), headers)

    # for item in items:
    #     print(item)
    # print(len(items))
    return items


# print(get_html(URL, HEADERS))
data = get_info(URL, HEADERS, 10)

data_file = open("data.json", "w")
json.dump(data, data_file)
data_file.close()

df = pd.DataFrame(data)
df.to_excel("data.xlsx")
