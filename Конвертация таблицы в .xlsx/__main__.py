import xml.etree.ElementTree as ET
import zipfile
import re
import sys
from tkinter import filedialog
from tkinter import Tk
from tkinter import messagebox
from datetime import datetime

REGEX_DATE = re.compile(r'\d{2}\.\d{2}\.\d{4}')

OFFICE_NS = '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}'
TABLE_NS = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}'
TEXT_NS = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'

messagebox.showinfo('Выбор входного файла', 'Для начала работы необходимо выбрать входной .odt файл')
input_file_path = filedialog.askopenfilename(filetypes=[('Файл ODT', '*.odt')])

if not input_file_path:
    sys.exit(0)

messagebox.showinfo('Сохранить файл', 'Теперь необходимо выбрать где будет сохранён результат')
output_file_path = filedialog.asksaveasfilename(filetypes=[('Файл CSV', '*.csv')], defaultextension='.csv')

if not output_file_path:
    sys.exit(0)


def get_full_text(e: ET.Element):
    result = e.text if e.text else ''
    for i in e.findall(f'./'):
        if i.tail:
            result += f' {i.tail}'
    return result.strip().replace('"', '')


class Person:

    def __init__(self, e: list[ET.Element]) -> None:

        # № п/п
        # регистрационный номер
        self.order_n, self.registration_n = map(get_full_text, e[0].findall(f'./{TEXT_NS}p')[:2])

        # ФИО, СНИЛС, дата рождения
        tmp = e[1].findall(f'./{TEXT_NS}p')
        self.full_name = get_full_text(tmp[0])
        self.snils = get_full_text(tmp[1])

        raw_date = get_full_text(tmp[2])
        self.date_of_birth = datetime.strptime(raw_date, '%d.%m.%Y') if REGEX_DATE.match(raw_date) else None

        # адрес регистрации
        self.registration_address = get_full_text(tmp[4])
        # адрес пребывания
        self.residential_address = get_full_text(tmp[6])
        # фактический адрес
        self.actual_address = get_full_text(tmp[8])

        tmp = e[2].findall(f'./{TEXT_NS}p')
        # дата приёма заявления
        raw_date = get_full_text(tmp[0])
        self.date_of_receipt = datetime.strptime(raw_date, '%d.%m.%Y') if REGEX_DATE.match(raw_date) else None
        # дата подачи
        raw_date = get_full_text(tmp[1])
        self.date_of_application = datetime.strptime(raw_date, '%d.%m.%Y') if REGEX_DATE.match(raw_date) else None
        
        # дата подачи доп. документов
        raw_date = get_full_text(e[3].find(f'./{TEXT_NS}p'))
        self.date_of_additional_documents = datetime.strptime(raw_date, '%d.%m.%Y') if REGEX_DATE.match(raw_date) else None

        # содержание заявления
        tmp = e[4].findall(f'./{TEXT_NS}p')
        self.application_content = ['', '', '', '']
        for k, v in enumerate(map(get_full_text, tmp[::2])):
            if k > 3:
                break
            self.application_content[k] = v

        # содержание решения
        tmp = e[5].findall(f'./{TEXT_NS}p')
        self.decision_content = ['', '']
        raw_decision = list(map(get_full_text, tmp[::2]))
        for k, v in enumerate(raw_decision):
            if k > 1:
                break
            self.decision_content[k] = v
        # дата решения
        self.decision_date = datetime.strptime(raw_decision[2], '%d.%m.%Y') if REGEX_DATE.match(raw_decision[2]) else None

        # размер выплаты
        tmp = get_full_text(e[6].find(f'./{TEXT_NS}p')).replace(',', '.').replace(' ', '')
        self.payment_amount = float(tmp) if (tmp and tmp != 'null') else None

        # срок выплаты с
        self.payment_term_from = datetime.strptime(tmp, '%d.%m.%Y') if (tmp := get_full_text(e[7].find(f'{TEXT_NS}p'))) else None
        # срок выплаты по
        tmp = get_full_text(e[8].find(f'{TEXT_NS}p'))
        self.payment_term_to = datetime.strptime(tmp, '%d.%m.%Y') if REGEX_DATE.match(tmp) else tmp if tmp else None

        # отказ в установлении выплаты
        self.refused = True if (tmp := get_full_text(e[9].find(f'{TEXT_NS}p'))) == 'Да' else False if tmp == 'Нет' else None


    def csv(self) -> str:

        result = f'"{self.order_n}","{self.registration_n}","{self.full_name}","{self.snils}",'

        if self.date_of_birth:
            result += f'{self.date_of_birth.strftime("%d.%m.%Y")},'
        else:
            result += ','

        result += f'"{self.registration_address}","{self.residential_address}","{self.actual_address}",'

        if self.date_of_receipt:
            result += f'{self.date_of_receipt.strftime("%d.%m.%Y")},'
        else:
            result += ','
        
        if self.date_of_application:
            result += f'{self.date_of_application.strftime("%d.%m.%Y")},'
        else:
            result += ','

        if self.date_of_additional_documents:
            result += f'{self.date_of_additional_documents.strftime("%d.%m.%Y")},'
        else:
            result += ','

        for i in self.application_content:
            if i:
                result += f'"{i}",'
            else:
                result += ','
        
        for i in self.decision_content:
            if i:
                result += f'"{i}",'
            else:
                result += ','

        if self.decision_date:
            result += f'{self.decision_date.strftime("%d.%m.%Y")},'
        else:
            result += ','

        if self.payment_amount:
            result += f'"{str(self.payment_amount).replace(".", ",")}",'
        else:
            result += ','
        
        if self.payment_term_from:
            result += f'{self.payment_term_from.strftime("%d.%m.%Y")},'
        else:
            result += ','
        
        if isinstance(self.payment_term_to, str):
            result += f'"{self.payment_term_to}",'
        elif self.payment_term_to:
            result += f'{self.payment_term_to.strftime("%d.%m.%Y")},'
        else:
            result += ','

        if self.refused == True:
            result += '"Да"'
        elif self.refused == False:
            result += '"Нет"'
        
        result += '\n'

        return result


persons: list[Person] = list()

with zipfile.ZipFile(input_file_path) as odt:
    with odt.open('content.xml') as content:
        rows = ET.parse(content).findall(f'./{OFFICE_NS}body/{OFFICE_NS}text/{TABLE_NS}table/{TABLE_NS}table-row')
        for row in rows[3:]:
            cells = row.findall(f'./{TABLE_NS}table-cell')
            persons.append(Person(cells))

with open(output_file_path, 'wt') as f:
    f.write('"№ п/п","Регистрационный номер","ФИО","СНИЛС","Дата рождения","Адрес регистрации","Адрес пребывания","Адрес факт.-го проживания","Дата приёма заявления","Дата подачи заявления","Дата подачи доп. документов","Содержание заявления","Содержание заявления 2","Содержание заявления 3","Содержание заявления 4","Содержание решения","Содержание решения 2","Дата принятия решения","Размер выплаты","Срок установления с","Срок установления по","Отказано в установлении"\n')
    for i in persons:
        f.write(i.csv())