import datetime
import csv
import re

FILES = [
    'data/raw/Мужчины.csv',
    'data/raw/Женщины.csv'
]


def cls():
    print('\033[2J\033[H', end='')


def snils_format(x: str):
    if len(x) == 11:
        try:
            return f'{x[:3]}-{x[3:6]}-{x[6:9]} {x[9:]}'
        except:
            return x
    else:
        return x


class Person:

    def __init__(self, parse: bool, ids, name, dob, address, EI, J, empty_checked = False) -> None:

        self.additional = ''
        self.empty_checked = empty_checked

        if parse:
            self.ids = set(filter(bool, map(lambda x: ''.join(filter(str.isdecimal, x)), re.split(r' {2,}', ids))))
            self.name = name.strip().replace('\n', '').replace('"', '').upper()
            self.dob = datetime.datetime.strptime(dob, '%d.%m.%Y')
            self.address = address.strip().replace('\n', '').replace('"', '')
            self.EI = EI.strip().replace('\n', '').replace('"', '')
            self.J = J.strip().replace('\n', '').replace('"', '')
        else:
            self.ids = ids
            self.name = name
            self.dob = dob
            self.address = address
            self.EI = EI
            self.J = J

    def csv(self) -> str:
        return f'"{", ".join(map(snils_format, self.ids))}","{self.name}",{self.dob},"{self.address}","{self.EI}","{self.J}","{self.additional}"'

    def __str__(self) -> str:
        return f'\tСНИЛС: "{", ".join(self.ids)}"\n\tИмя: "{self.name}"\n\tДата: {self.dob.strftime("%d.%m.%Y")}\n\tАдрес: "{self.address}"\n\tСтолбцы E-I: "{self.EI}"\n\tСтолбец J: "{self.J}"'


with open('data/raw/Мужчины.csv') as f1, open('data/raw/Женщины.csv') as f2:
    raw_males = list(csv.reader(f1))[1:]
    raw_females = list(csv.reader(f2))[1:]

males: list[Person] = list()
for k, v in enumerate(raw_males):
    males.append(Person(True, v[0], v[1], v[2], v[3], ', '.join(filter(bool, v[4:9])), v[9]))

females: list[Person] = list()
for k, v in enumerate(raw_females):
    females.append(Person(True, v[0], v[1], v[2], v[3], ', '.join(filter(bool, v[4:9])), v[9]))

males.sort(key=lambda x: len(x.ids), reverse=True)
females.sort(key=lambda x: len(x.ids), reverse=True)

for dataset_n, dataset in enumerate((males, females)):

    checked: set[str] = set()
    out: list[Person] = list()

    for person_n, person in enumerate(dataset):

        if person.ids and person.ids.issubset(checked) or person.empty_checked:
            continue

        clones: list[Person] = []
        for sub_person in dataset:
            if person is sub_person or sub_person.ids and sub_person.ids.issubset(checked):
                continue
            elif person.ids.intersection(sub_person.ids):
                clones.append(sub_person)

        checked.update(person.ids)

        cls()
        print(f'Файл #{dataset_n+1}')
        print(f'Строка #{person_n+1} из {len(dataset)}\n')

        if len(clones):

            candidates = [person, *clones]
            for candidate_n, candidate in enumerate(candidates):
                print(f'{candidate_n}.', candidate, end='\n\n')

            flag = True
            while flag:
                opt = input(f'[q] новая запись, [w] оставить все, [0]-[{len(candidates)-1}] оставить только выбранную: ')

                if opt == 'q':

                    opt = int(input(f'Номер записи, из которой сохранить СНИЛС: '))
                    ids = candidates[opt].ids

                    opt = int(input(f'Номер записи, из которой сохранить имя: '))
                    name = candidates[opt].name

                    opt = int(input(f'Номер записи, из которой сохранить дату: '))
                    dob = candidates[opt].dob

                    opt = int(input(f'Номер записи, из которой сохранить адрес: '))
                    address = candidates[opt].address

                    opt = int(input(f'Номер записи, из которой сохранить столбцы E-I: '))
                    EI = candidates[opt].EI

                    opt = int(input(f'Номер записи, из которой сохранить столбец J: '))
                    J = candidates[opt].J

                    new = Person(False, ids, name, dob, address, EI, J)
                    if len(new.ids) > 1:
                        new.additional = 'Несколько СНИЛС'

                    print('\n', new)
                    input()

                    out.append(new)
                    flag = False

                elif opt == 'w':
                    for i in candidates:
                        i.additional = 'Двойник по СНИЛС/дате рождения/адресу'
                    out.extend(candidates)
                    flag = False

                elif opt.isdecimal():
                    out.append(candidates[int(opt)])
                    flag = False

        else:
            if len(person.ids) > 1:
                person.additional = 'Несколько СНИЛС'
            out.append(person)

    with open(f'data/{dataset_n}.csv', 'w') as f:
        for i in out:
            f.write(f'{i.csv()}\n')
