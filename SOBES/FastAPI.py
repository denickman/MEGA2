import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


'''
1. Нет валидации типов данных

В исходном коде speed может прийти как строка "быстро" вместо числа, и код это молча проглотит — data["speed"] 
просто достанет строку, и в f-строке она окажется как есть, никакой ошибки не будет, хотя логически это неверные данные.

С Pydantic speed: float — FastAPI автоматически вернёт 422 Unprocessable Entity, если прислали не число.

2. Нет автоматической документации (OpenAPI/Swagger)

С data: dict в Swagger UI (/docs) будет написано просто "любой JSON-объект" — пользователь API не узнает, 
какие поля реально ожидаются, не видя код. С Pydantic-моделью Swagger сам сгенерирует точную схему со всеми полями и типами.

3. Дублирование кода — 4 раза одно и то же вместо валидации схемой
try:
    name = data["name"]
    team = data["team"]
    speed = data["speed"]
    country = data["country"]
except KeyError as e:
    raise HTTPException(status_code=400, detail=f"Missing field: {e.args[0]}")
    
    
    
4. Ошибка сообщает только про ОДНО отсутствующее поле за раз

Если в запросе не хватает сразу name и country, try/except поймает KeyError на первом же отсутствующем поле (name)
 и вернёт ошибку только про него. Пользователь API исправит name, отправит снова — и только тогда узнает, 
 что country тоже отсутствует. Это плохой UX — приходится чинить по одной ошибке за раз.

Pydantic в ответе на 422 вернёт сразу все проблемные поля одним списком:

{
  "detail": [
    {"loc": ["body", "name"], "msg": "field required"},
    {"loc": ["body", "country"], "msg": "field required"}
  ]
}

'''


# HTTP-статус 400 Bad Request означает: "запрос от клиента сформирован некорректно" — проблема на стороне того, кто отправил запрос, а не на стороне сервера.

@app.post('/create_racer')
async def create_racer(data: dict):
    try:
        name = data['name']
        team = data['team']
        speed = data['speed']
        country = data['country']
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'MIssing fiedls: {e.args[0]}')

    return {
        'message': f'Racer {name} from {team} ({country}): with speed {speed} km/h created'
    }




class RacerCreate(BaseModel):
    name: str
    team: str
    speed: float = Field(gt=0)
    country: str
    # НЕТ id, НЕТ created_at — клиент их не передаёт

class RacerResponse(BaseModel):
    id: int
    name: str
    team: str
    speed: float
    country: str
    created_at: datetime
    # ЕСТЬ id и created_at — сервер их возвращает после создания




@app.post('/racers')
async def create_racer(racer: RacerCreate):
    return {
        'message': f'Racer {racer.name} from {racer.team} ({racer.country}) with speed {racer.speed} km/h created'
    }

'''
@app.post('/racers', response_model=RacerResponse)
async def create_racer(racer: RacerCreate):
    # racer — это то, что ПРИСЛАЛ клиент (без id)
    new_racer = save_to_db(racer)  # сервер сам генерирует id, created_at
    return new_racer  # а вот ЭТО уже валидируется как RacerResponse
'''


