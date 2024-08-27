import pytesseract

from PIL import Image
from celery import Celery

from database import get_session_factory
from models import DocumentsText


pytesseract.pytesseract.tesseract_cmd = 'C:/soft/tesseract/tesseract.exe'
celery = Celery('analyse', broker='redis://localhost:6379')

@celery.task
def analyze(doc_item_id, doc_item_path):
    db_session = get_session_factory()

    image = Image.open(doc_item_path)
    image_text = pytesseract.image_to_string(image)

    doc_info = {'id_doc': doc_item_id, 'text': image_text}
    doc = DocumentsText(**doc_info)
    db_session.add(doc)
    db_session.commit()