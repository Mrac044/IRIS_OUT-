from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from config import USER_LOGIN, USER_PASSWORD, IMAGE_PATHS

app = FastAPI()

# Настройка шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# Импортируем функцию предсказания
try:
    from model import predict_iris
except ImportError:
    def predict_iris(sl, sw, pl, pw):
        return "setosa"

# Функция проверки авторизации
def is_authenticated(auth_cookie: str = None) -> bool:
    return auth_cookie == "authorized"

# Главная страница - редирект на авторизацию
@app.get("/")
async def root():
    return RedirectResponse("/login")

# Страница авторизации
@app.get("/login")
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error
    })

# Обработка авторизации
@app.post("/login")
async def login(request: Request, login: str = Form(...), password: str = Form(...)):
    if login == USER_LOGIN and password == USER_PASSWORD:
        response = RedirectResponse("/form", status_code=303)
        response.set_cookie(key="auth", value="authorized")
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверный логин или пароль!"
        })

# Страница с формой (только для авторизованных)
@app.get("/form")
async def form_page(request: Request, auth: str = Cookie(default=None)):
    if not is_authenticated(auth):
        return RedirectResponse("/login")
    
    return templates.TemplateResponse("form.html", {"request": request})

# Обработка формы предсказания
@app.post("/predict")
async def predict(
    request: Request,
    sl: float = Form(...),
    sw: float = Form(...),
    pl: float = Form(...),
    pw: float = Form(...),
    auth: str = Cookie(default=None)
):
    if not is_authenticated(auth):
        return RedirectResponse("/login")
    
    result = predict_iris(sl, sw, pl, pw)
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result,
        "sl": sl,
        "sw": sw,
        "pl": pl,
        "pw": "pwВлад"
    })

# Выход из системы
@app.get("/logout")
async def logout():
    response = RedirectResponse("/login")
    response.delete_cookie(key="auth")
    return response

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)