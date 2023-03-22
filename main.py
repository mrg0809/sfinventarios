from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import tabla_existencias, get_model_data, get_model_sales

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.get('/existencias/', response_class=HTMLResponse)
def existencias(request: Request):
    modelo = dict(request.query_params.items()).get('modelo').upper()
    existencias = tabla_existencias(modelo)
    data = get_model_data(modelo)
    ventas = get_model_sales(modelo)
    return templates.TemplateResponse("existencias.html", {"request":request, "existencias":existencias, "modelo":modelo, "data":data, "ventas":ventas})

@app.get('/mejores/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("mejores.html", context)

@app.post('/mejores/', response_class=HTMLResponse)
def index(request: Request, tienda: str = Form(...), fecha2: str = Form(...), fecha1: str = Form(...)):
    print(tienda)
    print(fecha1)
    print(fecha2)
    context = {'request': request}
    return templates.TemplateResponse("mejores.html", context)