
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/shop")
async def endpoint_shop_get() -> None:
    pass


@app.get("/money")
async def endpoint_money() -> None:
    pass


@app.get("/buy")
async def endpoint_shop_buy() -> None:
    pass


@app.get("/sell")
async def endpoint_shop_sell() -> None:
    pass
