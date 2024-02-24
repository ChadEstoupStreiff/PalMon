import requests
from fastapi import APIRouter

router = APIRouter(tags=["Palmon service"])


@router.get("/palmon")
async def endpoint_palmon_get(palmon_id: int) -> None:
    return requests.get(
        f"http://palmon_service_palmons:80/palmon?palmon_id={palmon_id}"
    ).json()


# @router.post("/palmon")
# async def endpoint_palmon_create() -> None:
#     return requests.post("http://palmon_service_palmons:80/palmon").json()


@router.put("/switch")
async def switch_bag_storage(user: str, palmon_id: int):
    return requests.put(
        f"http://palmon_service_palmons:80/switch?user={user}&palmon_id={palmon_id}"
    ).json()


@router.delete("/release")
async def endpoint_bag_delete(user: str, palmon_id: int):
    return requests.delete(
        f"http://palmon_service_palmons:80/release?user={user}&palmon_id={palmon_id}"
    ).json()


@router.get("/bag")
async def endpoint_bag_get(user: str) -> None:
    return requests.get(f"http://palmon_service_palmons:80/bag?user={user}").json()


@router.post("/bag")
async def endpoint_bag_post(user: str, palmon_id: int) -> bool:
    return requests.post(
        f"http://palmon_service_palmons:80/bag?user={user}&palmon_id={palmon_id}"
    ).json()


@router.get("/storage")
async def endpoint_storage_get(user: str) -> None:
    return requests.get(f"http://palmon_service_palmons:80/storage?user={user}").json()


@router.post("/storage")
async def endpoint_storage_post(user: str, palmon_id: int):
    return requests.post(
        f"http://palmon_service_palmons:80/storage?user={user}&palmon_id={palmon_id}"
    ).json()
