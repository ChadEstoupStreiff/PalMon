import requests
from fastapi import APIRouter

router = APIRouter(tags=["Egg service"])


@router.get("/egg")
async def endpoint_egg_get(user) -> int:
    return requests.get(f"http://palmon_service_eggs:80/egg?owner={user}").json()


@router.get("/date")
async def get_date() -> str:
    return requests.get("http://palmon_service_eggs:80/date").json()


# @router.post("/egg")
# async def endpoint_egg_create(user) -> None:
#     return requests.post(f"http://palmon_service_eggs:80/egg?owner={user}").json()


@router.get("/incubator")
async def endpoint_incubator_get(user: str) -> None:
    return requests.get(f"http://palmon_service_eggs:80/incubator?owner={user}").json()


# @router.post("/incubator")
# async def endpoint_incubator_create(user: str) -> bool:
#     return requests.post(f"http://palmon_service_eggs:80/incubator?owner={user}").json()


@router.post("/incubator/place")
async def endpoint_incubator_touch(user: str, incubator_id: int) -> bool:
    return requests.post(f"http://palmon_service_eggs:80/incubator/place?owner={user}&incubator_id={incubator_id}").json()


@router.post("/incubator/hatch")
async def endpoint_incubator_hatch(user: str, incubator_id: int):
    result = requests.post(f"http://palmon_service_eggs:80/incubator/hatch?owner={user}&incubator_id={incubator_id}").json()
    if result:
        return requests.post("http://palmon_service_palmons:80/palmon").json()
    return False
