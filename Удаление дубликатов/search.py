import csv
import datetime

class NVPiSVPerson:

    def __init__(self, n, id, name, gender, dob, on_pub_service, retirement_date, status, state) -> None:
        self.checked = False
        self.n = int(n)
        # self.id = ''.join(filter(str.isdecimal, id))
        self.id = id.strip()
        self.name = name
        self.gender = gender
        self.dob = datetime.datetime.strptime(dob, '%d.%m.%Y')
        self.on_pub_service = on_pub_service
        self.retirement_date = datetime.datetime.strptime(retirement_date, '%d.%m.%Y')
        self.status = status
        self.state = state
    
    def csv(self) -> str:
        return f'{self.n},"{self.id}","{self.name}","{self.gender}",{self.dob.strftime("%d.%m.%Y")},"{self.on_pub_service}",{self.retirement_date.strftime("%d.%m.%Y")},"{self.status}","{self.state}","{"Да" if self.checked else "Нет"}"\n'


class Person:

    def __init__(self, ids, name, dob) -> None:
        self.ids = ids.split(', ')
        self.name = name
        self.dob = datetime.datetime.strptime(dob, '%d.%m.%Y')


with open('data/raw/НВПиСВ.csv') as f1, open('data/0.csv') as f2, open('data/1.csv') as f3:
    raw_data_nvpisv = list(csv.reader(f1))[1:]
    raw_data_males = list(csv.reader(f2))
    raw_data_females = list(csv.reader(f3))


nvpisv: list[NVPiSVPerson] = list()
for i in raw_data_nvpisv:
    nvpisv.append(NVPiSVPerson(*i))

males: list[Person] = list()
for i in raw_data_males:
    males.append(Person(*i[:3]))

females: list[Person] = list()
for i in raw_data_females:
    females.append(Person(*i[:3]))


for i in males+females:
    for j in nvpisv:
        if j.id in i.ids or i.name == j.name and i.dob == j.dob:
            j.checked = True

with open('data/2.csv', 'w') as f:
    for i in nvpisv:
        f.write(i.csv())
