import time
from random import Random
from typing import List

from db import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from objects import BagSlot, Palmon, StorageSlot
from presets import Presets

time.sleep(5)
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
    rarity = Random().randint(1, 1000)
    if rarity > 995:
        preset = Presets.palmons_preset_legendary  # 0.5%
        rarity = "Legendary"
    elif rarity > 900:
        preset = Presets.palmons_preset_epic  # 9.5%
        rarity = "Epic"
    elif rarity > 600:
        preset = Presets.palmons_preset_rare  # 30%
        rarity = "Rare"
    else:
        preset = Presets.palmons_preset_common  # 60%
        rarity = "Common"
    preset = preset[Random().randint(0, len(preset) - 1)]
    palmon = Palmon(
        type=preset[0],
        lvl=1,
        exp=0,
        rarity=rarity,
        stat_hp=Random().randint(int(preset[1] * 0.9), int(preset[1] * 1.1)),
        stat_dmg=Random().randint(int(preset[2] * 0.9), int(preset[2] * 1.1)),
        stat_def=Random().randint(int(preset[3] * 0.9), int(preset[3] * 1.1)),
        stat_spd=Random().randint(int(preset[4] * 0.9), int(preset[4] * 1.1)),
    )
    commit = DB().get()
    commit.add(palmon)
    commit.commit()
    return DB().get().query(Palmon).order_by(Palmon.id.desc()).first()


@app.put("/switch", tags=["palmon"])
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


@app.delete("/release", tags=["palmon"])
async def endpoint_bag_delete(user: str, palmon_id: int):
    commit = DB().get()
    bag = (
        commit.query(BagSlot)
        .filter(BagSlot.owner == user)
        .filter(BagSlot.palmon_id == palmon_id)
        .first()
    )
    if bag:
        commit.delete(bag)

    storage = (
        commit.query(StorageSlot)
        .filter(StorageSlot.owner == user)
        .filter(StorageSlot.palmon_id == palmon_id)
        .first()
    )
    if storage:
        commit.delete(storage)

    commit.commit()
    return True


def get_bag_of(user: str) -> List[Palmon]:
    return DB().get().query(Palmon).join(BagSlot).filter(BagSlot.owner == user).all()


@app.get("/bag", tags=["bag"])
async def endpoint_bag_get(user: str) -> None:
    return get_bag_of(user)


@app.post("/bag", tags=["bag"])
async def endpoint_bag_post(user: str, palmon_id: int) -> bool:
    commit = DB().get()
    if (
        not (commit.query(BagSlot).filter(BagSlot.palmon_id == palmon_id).first())
        and not (
            commit.query(StorageSlot).filter(StorageSlot.palmon_id == palmon_id).first()
        )
        and len(get_bag_of(user)) < 6
    ):
        bag = BagSlot(owner=user, palmon_id=palmon_id)
        commit.add(bag)
        commit.commit()
        return True
    return False


def get_storage_of(user: str) -> List[Palmon]:
    return (
        DB()
        .get()
        .query(Palmon)
        .join(StorageSlot)
        .filter(StorageSlot.owner == user)
        .order_by(Palmon.lvl.desc())
        .order_by(Palmon.id.desc())
        .all()
    )


@app.get("/storage", tags=["storage"])
async def endpoint_storage_get(user: str) -> None:
    return get_storage_of(user)


@app.post("/storage", tags=["storage"])
async def endpoint_storage_post(user: str, palmon_id: int):
    commit = DB().get()
    if not (
        commit.query(BagSlot).filter(BagSlot.palmon_id == palmon_id).first()
    ) and not (
        commit.query(StorageSlot).filter(StorageSlot.palmon_id == palmon_id).first()
    ):
        storage = StorageSlot(owner=user, palmon_id=palmon_id)
        commit.add(storage)
        commit.commit()
        return True
    return False
