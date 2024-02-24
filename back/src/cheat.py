import requests
from fastapi import APIRouter

router = APIRouter(tags=["Cheats"])


@router.post("/cheat/eggs")
async def cheat_eggs(user: str, quantity: int):
    requests.post(
        f"http://palmon_service_eggs:80/egg?owner={user}&quantity={quantity}"
    ).json()


@router.post("/cheat/dollars")
async def cheat_dollars(user: str, amount: int):
    requests.post(
        f"http://palmon_service_shop:80/money?user={user}&amount={amount}"
    ).json()


@router.post("/cheat/palmon")
async def cheat_palmon(user: str, quantity: int):
    for _ in range(quantity):
        palmon = requests.post("http://palmon_service_palmons:80/palmon").json()
        _ = requests.post(
            f"http://palmon_service_palmons:80/storage?user={user}&palmon_id={palmon['id']}"
        ).json()


@router.post("/cheat/hatch")
async def cheat_hatch():
    return requests.post("http://palmon_service_palmons:80/palmon").json()
