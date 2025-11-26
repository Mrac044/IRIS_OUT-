from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Импортируем функцию предсказания
try:
    from model import predict_iris
except ImportError:
    # Запасной вариант если импорт не работает
    def predict_iris(sl, sw, pl, pw):
        return "setosa"  # всегда возвращает setosa для теста

# HTML форма
HTML_FORM = """
<html>
<head>
    <title>Классификатор Ирисов</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        .container { background: #f9f9f9; padding: 20px; border-radius: 10px; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #4CAF50; color: white; padding: 10px; border: none; width: 100%; margin-top: 10px; }
        .result { background: #e8f5e8; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌷 Классификатор Ирисов</h2>
        <form action="/predict" method="post">
            Длина чашелистика: <input type="number" step="0.1" name="sl" value="5.1" required><br>
            Ширина чашелистика: <input type="number" step="0.1" name="sw" value="3.5" required><br>
            Длина лепестка: <input type="number" step="0.1" name="pl" value="1.4" required><br>
            Ширина лепестка: <input type="number" step="0.1" name="pw" value="0.2" required><br>
            <button type="submit">Определить вид</button>
        </form>
    </div>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(HTML_FORM)

@app.post("/predict")
async def predict(
    sl: float = Form(...), 
    sw: float = Form(...), 
    pl: float = Form(...), 
    pw: float = Form(...)
):
    result = predict_iris(sl, sw, pl, pw)
    
    result_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }}
            .container {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
            .result {{ background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            a {{ display: block; text-align: center; padding: 10px; background: #4CAF50; color: white; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>✅ Результат: {result}</h2>
            <div class="result">
                <p><strong>Введенные параметры:</strong></p>
                <p>Длина чашелистика: {sl}</p>
                <p>Ширина чашелистика: {sw}</p>
                <p>Длина лепестка: {pl}</p>
                <p>Ширина лепестка: {pw}</p>
            </div>
            <a href="/">← Назад к форме</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(result_html)

# Добавляем возможность запуска напрямую
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)