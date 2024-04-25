import asyncio

from fastapi import Request, FastAPI, Header, Cookie, HTTPException, Query, Depends
from typing import Union, Optional
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

from pydantic import BaseModel, Field

from fastapi import Form, File, UploadFile
import sample

app = FastAPI(title="GiSon Win学习FastAPI框架", description="本应用是基于FastAPI搭建的支持ASGI和WSGI协议的WEB应用框架",
              version="1.0.0")


# 定义依赖项函数
def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


class Item(BaseModel):
    name: str = Field(..., title="Item Name", max_length=100)
    description: str = Field(None, title="Item Description", max_length=100)
    price: float = Field(..., title="Item Price", gt=0)
    # is_offer: Union[bool, None] = None
    tax: float = Field(None, title="Item Tax", ge=123)


@app.get("/", tags=["app首页入口示例"])
def read_root():
    return {"Hello": "World"}


@app.get("/direct/")
def redirect():
    return RedirectResponse(url="/items")


@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User_Agent": user_agent, "Session_Token": session_token}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    content = {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
    headers = {"X-Custom-Header": "GiSon Win header value"}
    return JSONResponse(content=content, headers=headers)
    # return {"item_id": item_id, "q": q}


@app.get("/items/validate/{item_id}")
def read_validate_item(item: Item, q: str = Query(..., max_length=10)):
    return {"item": item, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}


@app.post("/items/")
def create_item(
        name: str = Form(...),
        description: str = Form(None),
        price=Form(..., gt=0),
        tax=Form(..., gt=123)
):
    return {"name": name, "description": description, "price": price, "tax": tax}


def verity_token(token: str = Depends(common_parameters)):
    if token is None:
        raise HTTPException(status_code=400, detail="Token required")
    return token


# FastAPI提供了路径操作依赖项(Path Operation Dependencies)机制，允许你在路由处理函数之前或之后运行一些额外的逻辑。
# 依赖项(Dependencies),在路由函数执行之前或之后运行的可复用的函数或对象，通常被用于执行一些通用的逻辑，如身份验证，数据库连接，权限验证等。
# - 预处理(Before)依赖项：路由函数执行前运行，预处理输入数据，验证请求等
# - 后处理(After)依赖项：路由函数执行后运行，执行一些后处理逻辑，如日志记录，清理等。
# 下面是预处理实现
@app.get("/items/depends/")
async def depends(commons: dict = Depends(verity_token)):
    return commons


# 下面是后处理
async def after_request():
    print("after_request")


@app.get("/items/after/", response_model=dict)
async def after(request: dict = Depends(after_request)):
    return request


async def get_token():
    await asyncio.sleep(2)
    return "fake-token"


@app.get("/items/async/")
async def async_items(token: Optional[str] = Depends(get_token)):
    return token


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


# 路由函数接收一个UploadFile类型的文件参数。FASTAPI将负责处理文件上传，并将文件相关信息包装在UploadFile对象中，可获取文件名，内容类型等信息。
@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
    return {"file": file.filename}


# @app.get("/sample", response_class=HTMLResponse)
# async def get_response(request: Request):
#     return sample.templates.TemplateResponse("index.html", {"request": request})
