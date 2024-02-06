from db import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from objects import Thune
from presets import Preset

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/shop")
async def endpoint_shop_get():
    return {
        "sell": Preset.sell_prices,
        "buy": Preset.buy_prices,
    }


@app.get("/money")
async def endpoint_money(user: str):
    amount = DB().get().query(Thune).filter(Thune.owner == user).first()
    if amount is not None:
        return amount.amount
    return 0


@app.put("/buy")
async def endpoint_shop_buy(user: str, object: str) -> None:
    amount = DB().get().query(Thune).filter(Thune.owner == user).first()
    if (
        amount is not None
        and object in Preset.buy_prices
        and amount.amount >= Preset.buy_prices[object]
    ):
        commit = DB().get()
        amount = commit.query(Thune).filter(Thune.owner == user).first()
        amount.amount -= Preset.buy_prices[object]
        commit.add(amount)
        commit.commit()
        return True
    return False


@app.put("/sell")
async def endpoint_shop_sell(user: str, object: str) -> None:
    if object in Preset.sell_prices:
        commit = DB().get()
        amount = commit.query(Thune).filter(Thune.owner == user).first()
        if amount is not None:
            amount.amount += Preset.sell_prices[object]
        else:
            amount = Thune(owner=user, amount=Preset.sell_prices[object])
        commit.add(amount)
        commit.commit()
        return True
    return False
