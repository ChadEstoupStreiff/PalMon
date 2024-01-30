from random import Random
from typing import List

from db import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from objects import BagSlot, Palmon, StorageSlot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/palmons", tags=["palmon"])
# async def endpoint_palmon_get() -> None:
#     return DB().get().query(Palmon).all()


@app.get("/palmon", tags=["palmon"])
async def endpoint_palmon_get(palmon_id: int) -> None:
    return DB().get().query(Palmon).filter_by(id=palmon_id).all()


@app.post("/palmon", tags=["palmon"])
async def endpoint_palmon_create() -> None:
    max_hp = Random().randint(80, 120)
    palmon = Palmon(
        type="picmi",
        lvl=1,
        hp=max_hp,
        stat_hp=max_hp,
        stat_dmg=Random().randint(80, 120),
        stat_def=Random().randint(80, 120),
        stat_spd=Random().randint(80, 120),
    )
    commit = DB().get()
    commit.add(palmon)
    commit.commit()
    return DB().get().query(Palmon).order_by(Palmon.id.desc()).first()


@app.put("/switch", tags=["bag", "storage"])
async def switch_bag_storage(user: str, palmon_id: int):
    commit = DB().get()

    bag = (
        commit.query(BagSlot)
        .filter(BagSlot.owner == user)
        .filter(BagSlot.palmon_id == palmon_id)
        .first()
    )
    if bag:
        commit.delete(bag)
        commit.add(StorageSlot(owner=user, palmon_id=palmon_id))
        commit.commit()
        return True

    storage = (
        commit.query(StorageSlot)
        .filter(StorageSlot.owner == user)
        .filter(StorageSlot.palmon_id == palmon_id)
        .first()
    )
    if storage:
        if len(get_bag_of(user)) < 6:
            commit.delete(storage)
            commit.add(BagSlot(owner=user, palmon_id=palmon_id))
            commit.commit()
            return True

    return False


def get_bag_of(user: str) -> List[Palmon]:
    return DB().get().query(Palmon).join(BagSlot).filter(BagSlot.owner == user).all()


@app.get("/bag", tags=["bag"])
async def endpoint_bag_get(user: str) -> None:
    return get_bag_of(user)


@app.post("/bag", tags=["bag"])
async def endpoint_bag_post(user: str, palmon_id: int) -> bool:
    if len(get_bag_of(user)) < 6:
        bag = BagSlot(owner=user, palmon_id=palmon_id)
        commit = DB().get()
        commit.add(bag)
        commit.commit()
        return True
    return False


@app.delete("/bag", tags=["bag"])
async def endpoint_bag_delete(user: str, palmon_id: int):
    commit = DB().get()
    storage = (
        commit.query(BagSlot)
        .filter(BagSlot.owner == user)
        .filter(BagSlot.palmon_id == palmon_id)
        .first()
    )
    commit.delete(storage)
    commit.commit()
    return True


def get_storage_of(user: str) -> List[Palmon]:
    return (
        DB()
        .get()
        .query(Palmon)
        .join(StorageSlot)
        .filter(StorageSlot.owner == user)
        .all()
    )


@app.get("/storage", tags=["storage"])
async def endpoint_storage_get(user: str) -> None:
    return get_storage_of(user)


@app.post("/storage", tags=["storage"])
async def endpoint_storage_post(user: str, palmon_id: int):
    storage = StorageSlot(owner=user, palmon_id=palmon_id)
    commit = DB().get()
    commit.add(storage)
    commit.commit()
    return True


@app.delete("/storage", tags=["storage"])
async def endpoint_storage_delete(user: str, palmon_id: int) -> bool:
    commit = DB().get()
    storage = (
        commit.query(StorageSlot)
        .filter(StorageSlot.owner == user)
        .filter(StorageSlot.palmon_id == palmon_id)
        .first()
    )
    commit.delete(storage)
    commit.commit()
    return True
