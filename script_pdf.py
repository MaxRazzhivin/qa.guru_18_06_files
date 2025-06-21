import os.path
from pypdf import PdfReader

from script_os import TMP_DIR

reader = PdfReader(os.path.join(TMP_DIR, "resume.pdf"))

print(reader.pages)
print(len(reader.pages))
print(reader.pages[1].extract_text())
def test():
    assert "Zephyr - чек-листы, тест-кейсы, тест-сьюты, тест-раны" in reader.pages[1].extract_text()

print(os.path.getsize(os.path.join(TMP_DIR, "resume.pdf")))

assert os.path.getsize(os.path.join(TMP_DIR, "resume.pdf")) == 147501