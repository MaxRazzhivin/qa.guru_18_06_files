from zipfile import ZipFile

with ZipFile("tmp/test_zip") as zip_file:
    print(zip_file.namelist())   # Перечислит файлы, которые есть внутри архива
    text = zip_file.read("Hello.txt")  # Прочтет содержимое файла внутри архива
    print(text)
    zip_file.extract("Hello.txt", path="tmp")
