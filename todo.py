from beanie import PydanticObjectId
from fastapi import APIRouter, Request, Form, Query, Path, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates

from model import Todo, TodoItem

todo_router = APIRouter()  # todoRouter = new APIRouter(); 라우터이자 컨트롤러 통신수단?이라고 생각하면

# todo_list = []

# Jinja2 Template을 사용하기 위헤 선언
template = Jinja2Templates(directory="templates")


@todo_router.post("/todo")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    # todo = Todo()
    # todo.item = item
    # todo.id = len(todo_list) + 1
    # todo_list.append(todo)
    await todo.create()
    todo_list = await todo.find_all().to_list()
    return template.TemplateResponse(
        "todo.html",
        {"request": request, "todos": todo_list}
    )


@todo_router.get("/todo")
async def retrieve_todo(request: Request):
    todo_list = await Todo.find_all().to_list()
    return template.TemplateResponse(
        "todo.html",
        {"request": request, "todos": todo_list}
    )


# @todo_router.get("/todos")
# def retrieve_todos() -> dict:
#     return {"todos": todo_list}


@todo_router.get("/todo/{id}")
async def get_todo(request: Request, id: PydanticObjectId = Path(), ):
    todo = await Todo.get(id)
    if todo:
        # for todo in todo_list:
        #     if todo.id == id:
        return template.TemplateResponse(
            "todo.html",
            {"request": request, "todo": todo}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist.")


# todo = next((t for t in todo_list if t.id == id), None)


# 수정
@todo_router.put("/todo/{id}")
async def update_todo(id: PydanticObjectId, data: TodoItem) -> dict:
    # todo = await Todo.get(id)
    # update todo set item = '점심먹기' where id = ''
    todo = await Todo.find_one(Todo.id == id)
    if todo :
        todo.item = data.item
        await todo.save()
        return {"message": "Todo updated succesfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist.")


# raise 는 에러를 발생시키는 코드, 메세지로 나타내지 않고 에러로 나타냄
@todo_router.delete("/todo/{id}")
async def delete_todo(id: PydanticObjectId) -> dict:
    todo = await Todo.get(id)
    if todo:
        await todo.delete()
    # for todo in todo_list:
    #     if todo.id == id:
    #         todo_list.remove(todo)
        return {"message": "Todo updated succesfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist.")

    # 성공시 메시지 : Todo deleted successfully.
    # 실패시 메시지 : Todo deleted dosen't exist.
    # range(len(todo_list))
    # todo_list.pop(index)


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    await Todo.delete_all()
    # todo_list.clear()
    return {"message": "All Todos are deleted successfully."}
#
# insert update 사실상 이 두개가 비슷한 시스템이자 거의 똑같아서 upsert 라고 불림
# id가 없으면 insert 새롭게 만드는거기 때문에 id가 존재하면 update 업데할 id를 가져와서 수정하기때문
# delete 는 id만 필요