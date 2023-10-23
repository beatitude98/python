from typing import Union

from fastapi import FastAPI, Request, Form

from connect import Settings
from todo import todo_router
from fastapi.templating import Jinja2Templates
from joblib import load

app = FastAPI()

template = Jinja2Templates(directory="templates")
settings = Settings()


@app.on_event('startup')
async def init_db():
    await settings.initialize_database()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/lang")
def lang(request: Request):
    return template.TemplateResponse("lang.html", {"request": request})


@app.post("/lang")
def detect_lang(request: Request, text: str = Form()):
    text = text.lower()
    code_a, code_z = (ord('a'), ord('z'))
    cnt = [0 for i in range(26)]
    for ch in text:
        n = ord(ch) - code_a
        if 0 <= n < 26:
            cnt[n] += 1
    total = sum(cnt)
    freq = list(map(lambda n:n/total, cnt))
    clf = load('lang/freq.pkl')
    result = clf.predict([freq])
    lang_dic = {"en" : "영어", "fr" : "프랑스어",
                "id" : "인도네이사어", "tl" : "타갈로그어"}
    language = lang_dic[result[0]]
    return template.TemplateResponse(
        "lang.html",
        {"request": request,
         "language": language,
         "text":text
         })


app.include_router(todo_router)

#to do 와 같은 맵을 만든다고 가정
#/todo 이러한 요청이 들어왔을때 => select, insert,update, delete
#서비스 : 회원관리, 게시글관리, 할일관리, 공지사항관리, Q&A관리 , FAQ 관리 , 관리자 관리
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.get("/member/{mem_id}")
# def read_member(mem_id: int):
#     return {"member_id": mem_id}
