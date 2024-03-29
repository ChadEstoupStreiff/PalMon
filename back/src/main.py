from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import palmons

app.include_router(palmons.router)

import shop

app.include_router(shop.router)

import egg_rabbit

app.include_router(egg_rabbit.router)

import cheat

app.include_router(cheat.router)
