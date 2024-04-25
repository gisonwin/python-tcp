import pathlib
import threading
import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="title", version="v1.0.0",
              contact={"name": "GisonWin's email", "url": "mail.qq.com", "email": "gisonwin@qq.com"})

templates = Jinja2Templates(directory=str(pathlib.Path.cwd()) + "/../templates/")
statistics = StaticFiles(directory=str(pathlib.Path.cwd()) + "/../static/")


@app.get("/sample/", response_class=HTMLResponse)
def get_response(request: Request):
    cwd = str(pathlib.Path.cwd())
    print(cwd)
    var = 1988 / 0
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sync/")
def sync_function():
    time.sleep(10)
    print("thread id：", threading.current_thread().ident)
    return {"index": "sync"}
