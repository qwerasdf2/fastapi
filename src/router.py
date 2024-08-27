import base64, random, os

import binascii

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.exc import NoResultFound

from database import get_session_factory
from models import Documents, DocumentsText
from schemas import Image, Document
from tasks import analyze

# from fastapi_cache.decorator import cache
# @router.get("/asd")
# @cache(expire=30)
# def get_long_op():
    # time.sleep(2)
    # return "blablabla"


router = APIRouter()

@router.post('/upload_doc')
def upload_doc(image: Image, document: Document):
    try:
        rand_name = ''.join(random.sample(population='qwertyuiopasdfghjklzxcvbnm', k=5))
        document.path = 'C:/dev/it_mentor/fast api/documents/'+rand_name+'.jpg'

        if len(image.b64_text) != 0:
            decode_text = base64.decodebytes(image.b64_text)
            with open(document.path, 'wb') as f:
                f.write(decode_text)

            db_session = get_session_factory()
            doc = Documents(**document.dict())
            db_session.add(doc)
            db_session.commit()
            
            return {'status': 200, 'message': 'file uploaded'}
        else:
            raise(HTTPException)
    
    except binascii.Error:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': 'need base64'})
    except:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': ''})

@router.post('/doc_delete')
def doc_delete(doc_id: int):
    try:
        db_session = get_session_factory()
        del_item = db_session.query(Documents).get(doc_id)

        if del_item:
            os.remove(del_item.path)
            db_session.delete(del_item)
            db_session.commit()
        
            return {'status': 200, 'message': {'delete': del_item}}
        else:
            return {'status': 200, 'message': f'{doc_id} null'}
    
    except NoResultFound as sql_exc:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': sql_exc._message()})
    except:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': ''})

@router.post('/doc_analyse')
def doc_analyze(doc_id: int):
    try:
        db_session = get_session_factory()
        doc_item = db_session.query(Documents).get(doc_id)
        
        if doc_item:
            analyze.delay(doc_item.id, doc_item.path)
            
            return {'status': 200, 'doc_id': doc_id, 'message': 'success'}
        else:
            return {'status': 200, 'message': f'{doc_id} null'}
    
    except NoResultFound as sql_exc:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': sql_exc._message()})
    except:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': ''})

@router.get('/get_text')
def get_text(doc_id: int = 1, db_session = Depends(get_session_factory)): # ?? depends
    try:
        # db_session = get_session_factory()
        result = db_session.query(DocumentsText).where(DocumentsText.id_doc == doc_id).one()

        return {'status': 200, 'message': result}
    except NoResultFound as sql_exc:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': sql_exc._message()})
    except:
        raise HTTPException(status_code=400, detail={'status': 400, 'message': ''})