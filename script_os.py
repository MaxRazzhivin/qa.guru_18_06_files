import os.path
import shutil

# Путь до текущего запущенного файла
CURRENT_FILE = os.path.abspath(__file__)

# Путь до директории от этого файла
CURRENT_DIR = os.path.dirname(CURRENT_FILE)

# Склеиваем папки с новой папкой tmp

TMP_DIR = os.path.join(CURRENT_DIR, "tmp")

# Создание папки tmp2, если ее нет до этого

if not os.path.exists("tmp2"):
    os.mkdir("tmp2")

# Удаление папки tmp2 и всего содержимого

shutil.rmtree(os.path.join(CURRENT_DIR, "tmp2"))