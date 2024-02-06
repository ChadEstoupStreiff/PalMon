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
    return DB().get().query(Egg).filter_by(owner=owner).all()

@app.post("/egg", tags=["egg"])
async def endpoint_egg_create(egg_owner) -> None:
    palmon_count = DB().get().query(Egg).filter_by(owner=egg_owner).all()
    if not palmon_count:
        palmon_count.append(1)
    egg = Egg(
        owner=egg_owner, 
        amount = palmon_count[0]
    )
    commit = DB().get()
    commit.add(egg)
    commit.commit()