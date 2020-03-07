import csv

files = ['Гаражи.csv', 'Квартиры.csv', 'Коммерческая.csv', 'Комнаты.csv', 'Коттеджи.csv', 'Дачи.csv', 'Земля.csv']

with open("Аренда.csv", mode='w') as write_file:
    fieldnames = [
        "Регион", "Ссылка на объявление", "Продажа/Аренда",
        "Тип", "Широта/Долгота", "Площадь", "Этаж",
        "Цена", "название агенства недвижимости",
        "Ссылка на агенство", "Телефон агенства",
        "Дата скачивания"
    ]

    writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()

for file_name in files:
    with open(file_name, mode='r') as read_file, open("Аренда.csv", mode='a') as write_file:
        fieldnames = [
            "Регион", "Ссылка на объявление", "Продажа/Аренда",
            "Тип", "Широта/Долгота", "Площадь", "Этаж",
            "Цена", "название агенства недвижимости",
            "Ссылка на агенство", "Телефон агенства",
            "Дата скачивания"
        ]

        reader = csv.reader(read_file, delimiter=';')
        reader.__next__()

        writer = csv.DictWriter(write_file, delimiter=';', fieldnames=fieldnames)

        for row in reader:
            info = {
                "Регион": row[0],
                "Ссылка на объявление": row[1],
                "Продажа/Аренда": row[2],
                "Тип": row[3],
                "Широта/Долгота": row[4],
                "Площадь": row[5],
                "Этаж": row[6],
                "Цена": row[7],
                "название агенства недвижимости": row[8],
                "Ссылка на агенство": row[9],
                "Телефон агенства": row[10],
                "Дата скачивания": row[11],
            }

            writer.writerow(info)
