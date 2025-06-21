import os
import time

import requests
from selene import browser, query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from script_os import TMP_DIR

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": TMP_DIR,
    # директория по-умолчанию для файлов
    "download.prompt_for_download": False
    # опция чтобы не спрашивало подтверждения на скачивание
}

options.add_experimental_option('prefs',
                                prefs)  # добавляем нашу кастомную настройку в опции

driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"),
                          options=options)  # здесь скачиваем вебдрайвер и options - кастомизированная часть настроек для него

browser.config.driver = driver  # добавляем эту настройку в наш Селен

browser.open('https://github.com/pytest-dev/pytest/blob/main/README.rst')
# browser.element('[data-testid=download-raw-button]').click()
# time.sleep(5)

# вытащим ссылку для скачивания из элемента через атрибута href

href = browser.element('[data-testid="raw-button"]').get(
    query.attribute("href"))

# либо его аналог через Selenium
# elem = driver.find_element(By.CSS_SELECTOR, '[data-testid="raw-button"]')
# href = elem.get_attribute("href")

# скачаем теперь не браузером через элемент и клик, а через API
# через content получим бинарную строку(нули и единицы), которую дальше запишем в файл

content = requests.get(url=href).content

# сохраняем в файл - если его нет, то создастся и запишется в него

with open(os.path.join(TMP_DIR, "readme_2.rst"),
          "wb") as file:  # "wb" значит запись в бинарном формате
    file.write(content)


# сделаем проверку на наличие одной из строк в файле через чтение файла
# чтение "r" по-умолчанию идет в with open, можно не указывать
def test_text_in_downloaded_file():
    with open(os.path.join(TMP_DIR, "readme_2.rst")) as file:
        file_content_str = file.read()
        assert "test_answer" in file_content_str
