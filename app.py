from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

items = [
    {
        "id": 1,
        "descricao": "Notebook Dell"
    },
    {
        "id": 2,
        "descricao": "Teclado mecânico"
    },
    {
        "id": 3,
        "descricao": "Mouse sem fio"
    }
]

app = FastAPI()

class HealthResponse(BaseModel):
    status: int
    mensagem: str

class ConfigsResponse(BaseSettings):
    oi: str
    hw: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="ENV_"
    )

class ItemResponse(BaseModel):
    items: list[ItemList]

class ItemList(BaseModel):
    id: int
    descricao: str

templates = Jinja2Templates(directory="templates")

settings = ConfigsResponse()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request,name="index.html",context={"request": request})

@app.get("/health", response_model=HealthResponse)
async def status_aplicacao():
    return {"status": "200", "mensagem": "Aplicação funcionando xD"}

@app.get("/config/envs", response_model=ConfigsResponse)
async def config_envs():
    return settings

@app.get("/items", response_model=ItemResponse)
async def listar_items():
    return {"items": items}