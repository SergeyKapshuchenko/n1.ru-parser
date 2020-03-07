from requests_html import HTMLSession
import math
import csv


def parse_single_url(url):
    print("Starting scrapping url: " + url)

    all_urls = []
    host = url.split(".ru/")[0] + ".ru"

    with HTMLSession() as session:
        try:
            response = session.get(url=url)
        except BaseException:
            print("Can not connect to url: ", url)

    amount_of_pages = response.html.xpath("//li[@class='breadcrumbs-list__item'][4]")[0].text.split()[0]
    amount_of_pages = int(amount_of_pages)
    amount_of_pages = math.ceil(amount_of_pages / 100)

    print("Amount of pages: ", amount_of_pages)

    # Разкоментируйте один из single_page, смотря какой тип вы парсите
    # Справа указано под какой тип каждый из них

    # single_page = response.html.xpath(
    #     "//div[@class='card-title living-list-card__inner-block']//a[@target='_blank']/@href") # Комнаты / Квартиры / Коттеджи

    # single_page = response.html.xpath(
    #     "//div[@class='garages-list-card__col _main']//a[@target='_blank']/@href")       # для гаражей

    # single_page = response.html.xpath(
    #     "//div[@class='card-title commercial-list-card__inner-block']//a[@target='_blank']/@href")  # коммерческая

    # single_page = response.html.xpath(
    #     "//div[@class='card-title dacha-list-card__inner-block']//a[@target='_blank']/@href")  # дачи

    single_page = response.html.xpath(
        "//div[@class='card-title land-list-card__inner-block']//a[@target='_blank']/@href")  # земля

    all_urls += list(map(lambda x: host + x, single_page))

    for i in range(2, amount_of_pages + 1):
        with HTMLSession() as session:
            response = session.get(url=url + f"&page={i}")

        # Разкоментируйте один из single_page, смотря какой тип вы парсите
        # Справа указано под какой тип каждый из них

        # single_page = response.html.xpath(
        #     "//div[@class='card-title living-list-card__inner-block']//a[@target='_blank']/@href") # Комнаты / Квартиры / Коттеджи

        # single_page = response.html.xpath(
        #     "//div[@class='garages-list-card__col _main']//a[@target='_blank']/@href")    # для гаражей

        # single_page = response.html.xpath(
        #     "//div[@class='card-title commercial-list-card__inner-block']//a[@target='_blank']/@href")  # коммерческая

        # single_page = response.html.xpath(
        #     "//div[@class='card-title dacha-list-card__inner-block']//a[@target='_blank']/@href")  # дачи

        single_page = response.html.xpath(
            "//div[@class='card-title land-list-card__inner-block']//a[@target='_blank']/@href")  # земля

        all_urls += list(map(lambda x: host + x, single_page))

    print("Successfully done with scraping single url: " + url)
    print("Amount of parsed links: ", len(all_urls))
    return all_urls


def save_to_csv(read_from, save_to):
    """
    read_from: файл, с которого читаем ссылки на РЕГИОНЫ!
    save_to: файл, в который записываем все ссылки !
    """
    with open(read_from, mode='r') as read_file, open(save_to, mode='a') as write_file:
        reader = csv.reader(read_file, delimiter=';')
        reader.__next__()

        fieldnames = ['Регион', 'Ссылка на предложение']
        writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            region_name = row[0]
            region_url = row[1]

            links = parse_single_url(region_url)
            for link in links:
                writer.writerow({
                    'Регион': region_name,
                    'Ссылка на предложение': link
                })

    print("Successfully Done with saving all links to file")


save_to_csv("../zemlia_regions.csv", "arenda_zemlia.csv")
