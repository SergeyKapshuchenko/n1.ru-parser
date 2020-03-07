from requests_html import HTMLSession
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import csv

locker = Lock()

time = datetime.now().strftime("%Y-%m-%d")

write_to = "Земля.csv"
read_from = "../urls/arenda_zemlia.csv"


def crawler():
    with open(write_to, mode='w') as write_file:
        fieldnames = [
            "Регион", "Ссылка на объявление", "Продажа/Аренда",
            "Тип", "Широта/Долгота", "Площадь", "Этаж",
            "Цена", "название агенства недвижимости",
            "Ссылка на агенство", "Телефон агенства",
            "Дата скачивания"
        ]

        writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

    urls = []
    regions = []

    with open(read_from, mode='r') as read_file:
        reader = csv.reader(read_file, delimiter=';')
        reader.__next__()

        for row in reader:
            urls.append(row[1])
            regions.append(row[0])

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(parse_single_url, urls, regions)


def parse_single_url(url, region):
    with HTMLSession() as session:
        response = session.get(url=url)
        response = response.html

    try:
        location = response.xpath("//div[@class='offer-card-location-container']")[0].text
        location = ", ".join(location.split("\n"))
    except BaseException:
        location = "No information"

    area = "No information"
    floor = "No information"

    try:
        for value in response.xpath("//li[@class='card-land-content-params-list__item']"):
            text = value.text
            if "Площадь" in text:
                area = int(text.split('участка')[1].split()[0]) * 100
            elif "Этаж" in text:
                floor = text.split('Этаж')[1]
    except BaseException:
        pass

    try:
        who = response.xpath("//div[@class='offer-card-contacts__person _type']")[0].text + ", " + \
              response.xpath("//div[@class='offer-card-contacts__person']//span[@class='ui-kit-link__inner']")[0].text
    except BaseException:
        who = "No information"

    try:
        price = response.xpath("//div[@class='price']")[0].text.split("₽")[0].replace(" ", "")
    except BaseException:
        price = "No information"

    try:
        link = \
            response.xpath("//a[@class='ui-kit-link offer-card-contacts__owner-name _type-common _color-blue']/@href")[
                0]
    except IndexError:
        host = url.split(".ru/")[0] + ".ru"
        link = host + response.xpath(
            "//a[@class='ui-kit-link offer-card-contacts__link _agency-name _type-common _color-blue']/@href")[0]
    try:
        contacts = response.xpath("//a[@class='offer-card-contacts-phones__phone']/@href")[0].split("+")[1]
    except BaseException:
        contacts = "No information"

    info = {
        "Регион": region,
        "Ссылка на объявление": url,
        "Продажа/Аренда": "Аренда",
        "Тип": "Земля",
        "Широта/Долгота": location,
        "Площадь": area,
        "Этаж": floor,
        "Цена": price,
        "название агенства недвижимости": who,
        "Ссылка на агенство": link,
        "Телефон агенства": contacts,
        "Дата скачивания": time,
    }

    with locker:
        with open(write_to, mode='a') as write_file:
            fieldnames = [
                "Регион", "Ссылка на объявление", "Продажа/Аренда",
                "Тип", "Широта/Долгота", "Площадь", "Этаж",
                "Цена", "название агенства недвижимости",
                "Ссылка на агенство", "Телефон агенства",
                "Дата скачивания"
            ]

            writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)
            writer.writerow(info)


crawler()
