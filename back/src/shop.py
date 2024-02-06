import requests
from fastapi import APIRouter

router = APIRouter(tags=["Shop service"])


@router.get("/shop")
async def endpoint_shop_get():
    return requests.get("http://palmon_service_shop:80/shop").json()


@router.get("/money")
async def endpoint_money(user: str):
    return requests.get(f"http://palmon_service_shop:80/shop?user={user}").json()


@router.put("/buy")
async def endpoint_shop_buy(user: str, object: str) -> None:
    return requests.get(
        f"http://palmon_service_shop:80/shop?user={user}&object={object}"
    ).json()


@router.put("/sell")
async def endpoint_shop_sell(user: str, object: str) -> None:
    return requests.get(
        f"http://palmon_service_shop:80/shop?user={user}&object={object}"
    ).json()
