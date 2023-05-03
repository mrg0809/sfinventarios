from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from model.handle_db import tabla_existencias, get_model_data, get_model_sales, get_better_models, dashboard_data
from model.firebird import consultaVentaTiendaHoy
from controller.check_password import check_user
from starlette.status import HTTP_302_FOUND, HTTP_303_SEE_OTHER
import pandas as pd


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

templates = Jinja2Templates(directory="templates")



@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.post('/login', response_class=HTMLResponse)
def login(request: Request, username: str = Form(), password_user = Form()):
    verify = check_user(username, password_user)
    if verify:
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)


@app.get('/dashboard', response_class=HTMLResponse)
def index(request: Request):
    data = dashboard_data()
    venta = consultaVentaTiendaHoy()
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data, "venta": venta})

@app.get('/existencias/', response_class=HTMLResponse)
def existencias(request: Request):
    modelo = dict(request.query_params.items()).get('modelo').upper()
    existencias = tabla_existencias(modelo)
    try:
        data = get_model_data(modelo)
    except:
        data = {'descripcion': 'NO DATA', 'precio': 'NO DATA', 'descuento': 'NO DATA', 'precio_tienda': 'NO DATA', 'linea': 'NO DATA', 'marca': 'NO DATA', 'subcategoria' :'NO DATA', 'costo':'NO DATA'}
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

@app.get('/inventario', response_class=HTMLResponse)
def index(request: Request):
    data = 0
    return templates.TemplateResponse("inventario.html", {"request":request, "data": data})

