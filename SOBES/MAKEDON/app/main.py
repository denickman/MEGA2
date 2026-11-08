from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.models.base import Base
from app.db.session import engine
from app.api.routers.TaskRouter import router as task_router





# lifespan for fastapi
@asynccontextmanager
async def lifespan(_: FastAPI):
    # create tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








