import requests
from fastapi import APIRouter

router = APIRouter(tags=["Shop service"])


@router.get("/shop")
async def endpoint_shop_get():
    return requests.get("http://palmon_service_shop:80/shop").json()


@router.get("/money")
async def endpoint_money(user: str):
    return requests.get(f"http://palmon_service_shop:80/money?user={user}").json()


@router.put("/buy")
async def endpoint_shop_buy(user: str, object: str) -> bool:
    if object == "egg":
        result = requests.put(
            f"http://palmon_service_shop:80/buy?user={user}&object={object}"
        ).json()
        if result:
            return requests.post(
                f"http://palmon_service_eggs:80/egg?owner={user}"
            ).json()
    if object == "incubator":
        result = requests.get(
            f"http://palmon_service_eggs:80/incubator?user={user}"
        ).json()
        if len(result) < 6:
            result = requests.put(
                f"http://palmon_service_shop:80/buy?user={user}&object={object}"
            ).json()
            if result:
                return requests.post(
                    f"http://palmon_service_eggs:80/incubator?owner={user}"
                ).json()
    return False


@router.put("/sell")
async def endpoint_shop_sell(user: str, object: str) -> bool:
    if (
        object == "egg"
        and requests.get(f"http://palmon_service_eggs:80/egg?owner={user}").json() > 0
    ):
        _ = requests.put(
            f"http://palmon_service_shop:80/sell?user={user}&object={object}"
        )
        return requests.post(
            f"http://palmon_service_eggs:80/egg?owner={user}&quantity=-1"
        ).json()
    return False
