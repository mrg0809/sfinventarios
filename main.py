from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import tabla_existencias

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.get('/existencias/{modelo}', response_class=HTMLResponse)
def existencias(request: Request, modelo):
    data = tabla_existencias(modelo)
    return templates.TemplateResponse("existencias.html", {"request":request, "data":data})