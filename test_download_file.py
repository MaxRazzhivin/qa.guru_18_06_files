"""
Реализовал автотест на проверку скачивания и валидации содержимого файла с использованием Selenium + Selene + requests.
Настроил кастомную директорию скачивания через ChromeOptions. Использовал API-запрос вместо UI-клика для устойчивости теста.
Упаковал логику в переиспользуемые утилиты, обеспечив читаемость, масштабируемость и чистоту кода.

"""

import os
import requests
from selene import browser, query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from script_os import TMP_DIR

os.makedirs(TMP_DIR,
            exist_ok=True)  # Создадим директорию TMP_DIR, если ее нет. Если она есть, ошибка не возникнет


def create_browser_with_custom_download_dir():


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

    return driver



# Универсальная функция для скачивания через ссылку и создание файла с контентом
# Возвращает абсолютный путь к новому файлу
def download_file_via_href(href: str, filename: str):
    content = requests.get(url=href).content
    filepath = os.path.join(TMP_DIR, filename)
    with open(filepath, "wb") as file:
        file.write(content)
    return filepath

def test_file_dowloand_and_content_checked():
    browser.config.driver = create_browser_with_custom_download_dir()  # добавляем эту настройку в наш Селен

    try:
        browser.open('https://github.com/pytest-dev/pytest/blob/main/README.rst')

        # вытащим ссылку для скачивания из элемента через атрибута href

        href = browser.element('[data-testid="raw-button"]').get(query.attribute("href"))
        filepath = download_file_via_href(href, "readme_2.rst")

        assert os.path.exists(filepath), f"Файл не найден: {filepath}"

        with open(filepath, encoding='utf-8') as file:
            content = file.read()
            assert "pytest" in content.lower(), "Ожидаемый текст не найден в файле"

    finally:
        browser.quit()


# простой вариант функции выше ниже построчно

# href2 = browser.element('[data-testid="raw-button"]').get(
#     query.attribute("href"))

# либо его аналог через Selenium
# elem = driver.find_element(By.CSS_SELECTOR, '[data-testid="raw-button"]')
# href = elem.get_attribute("href")

# # скачаем теперь не браузером через элемент и клик, а через API
# # через content получим бинарную строку(нули и единицы), которую дальше запишем в файл
#
# content = requests.get(url=href2).content
#
# # сохраняем в файл - если его нет, то создастся и запишется в него
#
# with open(os.path.join(TMP_DIR, "readme_2.rst"),
#           "wb") as file:  # "wb" значит запись в бинарном формате
#     file.write(content)
#
#
# # сделаем проверку на наличие одной из строк в файле через чтение файла
# # чтение "r" по-умолчанию идет в with open, можно не указывать
# def test_text_in_downloaded_file():
#     with open(os.path.join(TMP_DIR, "readme_2.rst")) as file:
#         file_content_str = file.read()
#         assert "test_answer" in file_content_str
