from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model.handle_db import tabla_existencias, get_model_data, get_model_sales, get_better_models, dashboard_data
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.get('/dashboard', response_class=HTMLResponse)
def index(request: Request):
    data = dashboard_data()
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data})

@app.get('/existencias/', response_class=HTMLResponse)
def existencias(request: Request):
    modelo = dict(request.query_params.items()).get('modelo').upper()
    existencias = tabla_existencias(modelo)
    data = get_model_data(modelo)
    ventas = get_model_sales(modelo)
    return templates.TemplateResponse("existencias.html", {"request":request, "existencias":existencias, "modelo":modelo, "data":data, "ventas":ventas})

@app.get('/mejores/', response_class=HTMLResponse)
def index(request: Request):
    data = pd.DataFrame()
    return templates.TemplateResponse("mejores.html", {"request":request, "data": data})

@app.post('/mejores/', response_class=HTMLResponse)
def index(request: Request, tienda: str = Form(...), fecha2: str = Form(...), fecha1: str = Form(...)):
    data = get_better_models(tienda, fecha1, fecha2)
    return templates.TemplateResponse("mejores.html", {"request":request, "data": data})

@app.get('/inventario/', response_class=HTMLResponse)
def index(request: Request):
    data = 0
    return templates.TemplateResponse("inventario.html", {"request":request, "data": data})