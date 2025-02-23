import pytest, os.path, zipfile, shutil


CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
TMP_DIR = os.path.join(CURRENT_DIR, "..", "tmp")
DIR_ARCHIVE = os.path.join(CURRENT_DIR, "archives")
ARCHIVE_NAME = "archive.zip"
ARCHIVE_FILE_PATH = os.path.join(DIR_ARCHIVE, ARCHIVE_NAME)


@pytest.fixture(scope='session', autouse=True)
def zip_archive_create():
    if not os.path.exists(DIR_ARCHIVE):
        os.mkdir(DIR_ARCHIVE)

    archive_path = os.path.join(DIR_ARCHIVE, ARCHIVE_NAME)

    with zipfile.ZipFile(archive_path, "w") as archive:
        if os.path.exists(TMP_DIR):
            for file in os.listdir(TMP_DIR):
                file_path = os.path.join(TMP_DIR, file)
                if os.path.isfile(file_path):
                    archive.write(file_path, file)

    yield

    shutil.rmtree(os.path.join(DIR_ARCHIVE))

#
# print(CURRENT_FILE)
# print(CURRENT_DIR)
# print(TMP_DIR)
# print(DIR_ARCHIVE)