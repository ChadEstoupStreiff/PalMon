import requests
from fastapi import APIRouter

router = APIRouter(tags=["Palmon service"])


@router.get("/egg", tags=["egg"])
async def endpoint_egg_get(owner) -> int:
    return requests.get(f"http://palmon_service_eggs:80/egg?owner={owner}").json()


@router.get("/date", tags=["date"])
async def get_date() -> str:
    return requests.get("http://palmon_service_eggs:80/date").json()


@router.post("/egg", tags=["egg"])
async def endpoint_egg_create(owner) -> None:
    return requests.post(f"http://palmon_service_eggs:80/egg?owner={owner}").json()


@router.get("/incubator", tags=["incubator"])
async def endpoint_incubator_get(owner: str) -> None:
    return requests.get(f"http://palmon_service_eggs:80/incubator?owner={owner}").json()


@router.post("/incubator", tags=["incubator"])
async def endpoint_incubator_create(owner: str) -> bool:
    return requests.post(f"http://palmon_service_eggs:80/incubator?owner={owner}").json()


@router.post("/incubator/place", tags=["incubator"])
async def endpoint_incubator_touch(owner: str, incubator_id: int) -> bool:
    return requests.post(f"http://palmon_service_eggs:80/incubator/place?owner={owner}&incubator_id={incubator_id}").json()


@router.post("/incubator/hatch", tags=["incubator"])
async def endpoint_incubator_hatch(owner: str, incubator_id: int) -> bool:
    return requests.post(f"http://palmon_service_eggs:80/incubator/hatch?owner={owner}&incubator_id={incubator_id}").json()
