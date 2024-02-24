from datetime import datetime, timedelta

from db import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from objects import Egg, Incubator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_eggs(owner: str):
    return DB().get().query(Egg).filter_by(owner=owner).first()


@app.get("/egg", tags=["egg"])
async def endpoint_egg_get(owner) -> int:
    result = get_eggs(owner)
    if result is not None:
        return result.amount
    commit = DB().get()
    egg = Egg(owner=owner, amount=2)
    commit.add(egg)
    commit.commit()
    return 1


def push_egg(owner: str, amount: int) -> bool:
    commit = DB().get()
    egg = commit.query(Egg).filter_by(owner=owner).first()
    if egg is not None:
        egg.amount += amount
    else:
        egg = Egg(owner=owner, amount=1 + amount)
    commit.add(egg)
    commit.commit()
    return True


@app.get("/date", tags=["date"])
async def get_date() -> str:
    return str(datetime.now())


@app.post("/egg", tags=["egg"])
async def endpoint_egg_create(owner, quantity: int = 1) -> bool:
    return push_egg(owner, quantity)


def get_incubators(owner: str):
    result = DB().get().query(Incubator).filter_by(owner=owner).all()
    if result is not None:
        return result
    return []


def create_incubator(owner: str):
    commit = DB().get()
    incubator = Incubator(
        owner=owner,
        occupied=False,
        hatch_date=None,
    )
    commit.add(incubator)
    commit.commit()


@app.get("/incubator", tags=["incubator"])
async def endpoint_incubator_get(owner: str):
    incubators = get_incubators(owner)
    if len(incubators) == 0:
        create_incubator(owner)
        return get_incubators(owner)
    return incubators


@app.post("/incubator", tags=["incubator"])
async def endpoint_incubator_create(owner: str) -> bool:
    incubators = get_incubators(owner)
    if incubators is not None and len(incubators) < 6:
        create_incubator(owner)
        return True
    return False


@app.post("/incubator/place", tags=["incubator"])
async def endpoint_incubator_touch(owner: str, incubator_id: int) -> bool:
    if get_eggs(owner).amount > 0:
        incubator = (
            DB()
            .get()
            .query(Incubator)
            .filter_by(owner=owner)
            .filter_by(incubator_id=incubator_id)
            .first()
        )
        if incubator is not None and not incubator.occupied:
            push_egg(owner, -1)
            commit = DB().get()
            incubator = (
                commit.query(Incubator)
                .filter_by(owner=owner)
                .filter_by(incubator_id=incubator_id)
                .first()
            )
            incubator.occupied = True
            incubator.hatch_date = datetime.now() + timedelta(days=1)
            commit.commit()
            return True
    return False


@app.post("/incubator/hatch", tags=["incubator"])
async def endpoint_incubator_hatch(owner: str, incubator_id: int) -> bool:
    commit = DB().get()
    incubator = (
        commit.query(Incubator)
        .filter_by(owner=owner)
        .filter_by(incubator_id=incubator_id)
        .first()
    )
    if (
        incubator is not None
        and incubator.occupied
        # and incubator.hatch_date <= datetime.now()
    ):
        incubator.occupied = False
        incubator.hatch_date = None
        commit.commit()
        return True
    return False
