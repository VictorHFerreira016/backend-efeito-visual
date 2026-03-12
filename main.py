from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import servicos, produtos

app = FastAPI(
    title = "salao_de_beleza"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(servicos.router)
app.include_router(produtos.router)

'''if __name__ == "__main__":
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 5000
    )'''