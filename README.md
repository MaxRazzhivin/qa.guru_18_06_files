# Работа с файлами 


## Добавляем код, чтобы файл скачивался в определенную папку в проекте

```bash
- создаем папку для файлов tmp 

options = webdriver.ChromeOptions() // import из Selenium webdriver
prefs = {
  'download.default_directory': '/Users/maxnovo/Desktop/qa.guru/qa.guru_18_06/tmp', // директория по-умолчанию для файлов
  'download.prompt_for_download' = False // опция чтобы не спрашивало подтверждения на скачивание 
}

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options) // здесь скачиваем вебдрайвер и options - кастомизированная часть настроек для него

browser.config.driver = driver
```

## Как скачать файл в нужную директорию

Пример теста для скачивания файлов для версии Selene 2.0.0rc6 и выше. В тесте указан путь как абсолютный.

```bash
import time

from selene import browser
from selenium import webdriver


def test_text_in_downloaded_file_by_click():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": r"C:\Users\путь к вашей папке куда нужно скачать",  # пример пути указан для windows, если нужно для mac или linux, то путь будет другой, а именно /Users/имя пользователя/путь к папке
        "download.prompt_for_download": False
    }
    options.add_experimental_option("prefs", prefs)
    browser.config.driver_options = options

    browser.open("https://github.com/pytest-dev/pytest/blob/main/README.rst")
    browser.element("[data-testid='download-raw-button']").click()
    time.sleep(4)
```

Если на сайте не отображена кнопка для скачивания файла, но есть ссылка, то можно скачать его через api. 
Пример теста для скачивания файла через api: Для того чтобы работало скачивание файла через api, необходимо установить библиотеку requests. 
Команда для установки через терминал pip install requests.

```bash
import time
import requests

from selene import browser, query


def test_text_in_downloaded_file_by_click():
    browser.open("https://github.com/pytest-dev/pytest/blob/main/README.rst")
    download_url = browser.element("[data-testid='raw-button']").get(query.attribute("href")) # получаем ссылку на файл
    
    content = requests.get(url=download_url).content # скачиваем файл
    
    with open(r"C:\Users\путь к вашей папке куда нужно скачать\readme.rst", "wb") as file: # пример пути указан для windows, если нужно для mac или linux, то путь будет другой, а именно /Users/имя пользователя/путь к папке куда нужно скачать. wb - запись в бинарном режиме
        file.write(content)
        
    # если нужно проверить содержимое файла то ниже пример как это сделать
    with open(r"C:\Users\путь к вашей папке куда нужно скачать\readme.rst") as file: # пример пути указан для windows, если нужно для mac или linux, то путь будет другой, а именно /Users/имя пользователя/путь к папке куда нужно скачать. r - чтение файла
        file_content_str = file.read() # читаем содержимое файла
        assert "test_answer" in file_content_str  # проверяем содержимое файла, если в файле есть слово "test_answer"

```

with open - это контекстный менеджер, который автоматически закрывает файл после выполнения блока кода. 
В данном случае файл открывается для записи в бинарном режиме. Если файл с таким именем уже существует, то он будет перезаписан. 
Если нужно дописать в файл, то нужно использовать режим "a" вместо "w".


## Работа контекстным менеджером

```bash
with open('example.txt', 'w') as f: # открываем(создаем если он не создан ранее) файл для записи
    f.write('abc') # записываем строку 'abc' в файл
    
    # буква 'w' означает записать,если файл с таким именем уже существует, то он будет перезаписан
    # буква 'r' означает прочитать
    # буква 'a' означает дописать
    # буква 'x' означает записать только один раз и дальше запрещает запись. Если попытаться записать в файл второй раз, то будет ошибка
    
>>> with open('example.txt') as f: # открываем файл для чтения, буква 'r' можно не указывать, так как по умолчанию файл открывается для чтения
...     for row in f: # читаем файл построчно
...         print(row) # печатаем содержимое файла
abc

>>> with open('example.txt', 'a') as f: # открываем файл для дописывания
...     f.write('defg\n') # дописываем строку 'defg' в файл и переходим на новую строку
...     print(example.txt)
abc
defg
    
>>> with open('example.txt', 'x') as f: # открываем файл для записи
...     f.write('ghi') # записываем строку 'ghi' в файл

FileExistsError: [Errno 17] File exists: 'example.txt'


```

## Работа с путями

Для работы с путями в Python используется библиотека os. Она встроена в Python, поэтому устанавливать её не нужно.


```bash
import os

CURRENT_FILE = os.path.abspath(__file__) # получаем абсолютный путь к текущему файлу
CURRENT_DIRECTORY = os.path.dirname(CURRENT_FILE  ) # получаем абсолютный путь к текущей директории где находится файл с которым работаем
TMP_DIR = os.path.join(CURRENT_DIRECTORY, 'tmp') # делаем склейку пути к текущей директории и папки tmp
```

Константу TMP_DIR можно подставить в тесты, вместо пути к папке, чтобы не писать каждый раз путь в тестах.

```bash
download.default_directory = TMP_DIR

# а также при работе с файлом
with open(TMP_DIR+"/readme.rst, "wb") as file: 
```

Более лаконичный и короткий способ, для того чтобы получить путь к файлу:

```bash
os.getcwd() # получаем текущую директорию

Далее можно использовать полученный путь для работы с файлами
file_path = os.path.join(os.getcwd(), "tmp", "readme2.rst") # склеиваем путь к файлу readme2.rst
dir_path = os.path.join(os.getcwd(), "tmp") # склеиваем путь к папке tmp
```

## Работа с архивами

Для работы с архивами понадобится библиотека zipfile, которая встроена в Python.


```bash
from zipfile import ZipFile

# открываем архив
zip_ = ZipFile('путь/к/файлу/файл.zip')

# печатаем названия файлов в архиве
print(zip_.namelist())

# извлекаем файл из архива с указанием директории
zip_.extract('файл.txt', 'tmp')

# извлекаем все файлы из архива в директорию
zip_.extractall('tmp')

# читаем содержимое файла и печатаем его
text = zip_.read('файл.txt')
print(text)
zip_.close()
```

## Как работать с PDF

Для работы с PDF понадобится библиотека PyPDF, которая устанавливается с помощью команды pip install pypdf. 
PdfReader - это класс, который позволяет читать pdf-файлы.

```bash
from pypdf import PdfReader

reader = PdfReader("путь к файлу/файл.pdf")


number_of_pages = len(reader.pages)  # узнаем количество страниц в файле
print(number_of_pages)


# Читаем PDF-файл:
page = reader.pages[0] # получаем первую страницу
text = page.extract_text() # извлекаем текст из первой страницы 
print(text)

# Получаем текст из всех страниц:
for page in reader.pages:
    print(page.extract_text())

# Получаем текст из определенного диапазона страниц:
for page in reader.pages[0:2]:
    print(page.extract_text())
```

## Как работать с TXT

Записываем строку в txt-файл:

```bash
# Создаем файл и даем ему имя
f = open('example.txt', 'w')
# Передаем строку для записи в файл
f.write('abc')
f.close()
```

Считываем строку файла:

```bash
f = open('example.txt')
for row in f:
    print(row)
```

## Как работать с CSV

Для работы с csv-файлами необходимо использовать библиотеку csv. Она встроена в Python, подключить её можно с помощью строки import csv.

Построчная печать файла:

```bash
import csv

with open('путь/к/файлу/файл.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

Напечатать только одну колонку:

```bash
with open('tmp/username.csv') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        print(row['Username'])
```

Если нужно проверить содержимое файла, не распаковывая архив, то можно использовать следующий код:

```bash
import zipfile
import csv

def test_csv():
    with zipfile.ZipFile('путь/к/файлу/файл.zip') as zip_file: # открываем архив
        with zip_file.open('файл.csv') as csv_file: # открываем файл в архиве
            content = csv_file.read().decode('utf-8-sig') # читаем содержимое файла и декодируем его если в файле есть символы не из английского алфавита
            csvreader = list(csv.reader(content.splitlines())) # читаем содержимое файла и преобразуем его в список
            second_row = csvreader[1] # получаем вторую строку

            assert second_row[0] == '2'  # проверка значения элемента в первом столбце второй строки
            assert second_row[1] == 'b'  # проверка значения элемента во втором столбце второй строки

или

from io import TextIOWrapper


def test_csv_2():
    with zipfile.ZipFile('путь/к/файлу/файл.zip') as zip_file: # открываем архив
        with zip_file.open('файл.csv') as csv_file: # открываем файл в архиве 
            csvreader = list(csv.reader(TextIOWrapper(csv_file, 'utf-8-sig'))) # читаем содержимое файла и преобразуем его в список и декодируем его если в файле есть символы не из английского алфавита
            second_row = csvreader[1] # получаем вторую строку

            assert second_row[0] == '2' # проверка значения элемента в первом столбце второй строки
            assert second_row[1] == 'b' # проверка значения элемента во втором столбце второй строки
```

## Как работать с XLS и XLSX

Для работы с xlsx-файлами необходимо использовать библиотеку openpyxl. Установить её можно с помощью команды pip install openpyxl.

```bash
from openpyxl import load_workbook


workbook = load_workbook('путь/к/файлу/файл.xlsx') # открываем файл
 
sheet = workbook.active # получаем активный лист

print(sheet.cell(row=3, column=2).value) # печатаем содержимое строки и колонки

for row in sheet.iter_rows(): # получаем все строки и печатаем их
    print(row)

for column in sheet.iter_cols(): # получаем все колонки и печатаем их
    print(column)

for row in sheet.iter_rows():  # печатаем содержимое всех ячеек
    for cell in row:
        print(cell.value)
```

Для работы с xls-файлами необходимо использовать библиотеку xlrd. Установить её можно с помощью команды pip install xlrd.

```bash
import xlrd

book = xlrd.open_workbook('путь/к/файлу/файл.xls')

print(book.nsheets) # печать количества страниц

print(book.sheet_names()) # печать названия страницы

sheet = book.sheet_by_index(0) # вызвать лист по индексу

print(f'Количество столбцов {sheet.ncols}') # печать с листа количество столбцов

print(f'Количество строк {sheet.nrows}') # печать с листа количество строк

print(f'Ячейка 9:1 = {sheet.cell_value(rowx=9, colx=1)}') # печать содержимого ячейки

for rx in range(sheet.nrows): # печать содержимого всех ячеек
    print(sheet.row(rx))
```

Если необходимо отобразить данные из файла в табличном виде, то можно использовать библиотеку pandas. 
Установить её можно с помощью команды pip install pandas и pip install pyarrow.

```bash
import pandas as pd

df = pd.read_excel("tmp/file_example_XLSX_50.xlsx") # Чтение файла

print(df) # Выводим данные

print(df.head()) # Выводим первые 5 рядов

print(df.tail()) # Выводим последние 5 рядов

print(df.info()) # Выводим информацию о данных
```

## Как работать с ZIP

Для работы с zip-файлами необходимо использовать библиотеку zipfile. Она встроена в Python.

```bash
from zipfile import ZipFile


with ZipFile("путь/к/файлу/файл.zip") as zip_file: # открываем архив
    print(zip_file.namelist()) # печатаем названия файлов в архиве
    text = zip_file.read('файл.txt') # читаем содержимое файла
    zip_file.extract('Python Testing with Pytest (Brian Okken).pdf', path="tmp2") # извлекаем файл из архива с указанием директории
    zip_file.extractall('tmp2') # извлекаем все файлы из архива в директорию tmp2

# если нужно создать архив

with ZipFile("путь/к/файлу/файл.zip", 'w') as zip_file: # создаем архив
    zip_file.write("путь к файлу", arcname='название файла в архиве') # добавляем файл в архив
    zip_file.close() # закрываем архив
```

Если вам нужно запаковать несколько файлов в архив, то можно использовать следующий код:

```bash
import zipfile


def create_archive():
    if not os.path.exists('название папки в которой будет архив и его путь'): # проверяем существует ли папка
        os.mkdir('название папки в которой будет архив и его путь') # создаем папку если её нет
    with zipfile.ZipFile('название файла для архива и его путь', 'w') as zf: # создаем архив
        for file in 'файлы которые нужно добавить в архив': : # добавляем файлы в архив
            add_file = os.path.join('путь к файлам которые добавляют в архив', file) # склеиваем путь к файлам которые добавляют в архив
            zf.write(add_file, os.path.basename(add_file)) # добавляем файл в архив
    yield
    
    удаление_файлов_после_архивации() # удаляем файлы после архивации

```

## Удаление файлов и папок

Для удаления файлов и папок используется библиотека os. Она встроена в Python, поэтому устанавливать её не нужно.

```bash
import os

os.remove('example.txt') # удаляем файл
os.rmdir('tmp') # удаляем папку


import shutil

shutil.rmtree('путь к папке') # удаляем папку со всеми файлами и подпапками

```

Важно: Будьте осторожны с удалением файлов и папок через shutil , так как удалённые файлы и папки нельзя восстановить. 
Поэтому перед удалением файлов и папок убедитесь, что вы действительно удаляете ту папку или файл, который вам нужно удалить.