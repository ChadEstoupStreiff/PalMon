from random import Random
from typing import List

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

@app.get("/egg", tags=["egg"])
async def endpoint_egg_get(owner) -> None:
    result = DB().get().query(Egg).filter_by(owner=owner).first()
    if result is not None:
        return result.amount
    return 0

@app.post("/egg", tags=["egg"])
async def endpoint_egg_create(egg_owner) -> None:
    commit = DB().get()
    egg = commit.query(Egg).filter_by(owner=egg_owner).first()
    if egg is not None:
        egg.amount += 1
    else:
        egg = Egg(
            owner = egg_owner, 
            amount = 1
        )
    commit.add(egg)
    commit.commit()