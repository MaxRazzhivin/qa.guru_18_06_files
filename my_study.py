"""
📌 ЗАДАЧА:
	1.	Создай папку test_dir рядом с текущим .py файлом
	2.	Внутри test_dir создай файл info.txt
	3.	Запиши в этот файл строку:

	Hello, QA Automation!

	4.	Проверь, что файл существует
	5.	Выведи путь до файла и его содержимое в консоль
"""
import os

from script_os import CURRENT_DIR

test_dir = os.path.join(CURRENT_DIR, "test_dir")
if not os.path.exists(test_dir):
    os.mkdir(test_dir)

with open(os.path.join(test_dir, "info.txt"), "w") as file:
    file.write("Hello, QA Automation!")

file_path = os.path.join(test_dir, "info.txt")


if os.path.exists(file_path):
    print("✅ Файл существует!")
else:
    print("❌ Файл не найден!")

# Альтернатива через os.path
# os.path.isfile(file_path) - так именно проверка, что файл, а не папка

print(file_path)

with open(file_path) as file:
    print(file.read())

