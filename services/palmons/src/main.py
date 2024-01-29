
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/bag", tags=["bag"])
async def endpoint_bag_get(user: str) -> None:
    return None

@app.post("/bag", tags=["bag"])
async def endpoint_bag_post(user: str, palmon: Dict[str, Any]) -> None:
    return None

@app.put("/bag", tags=["bag"])
async def endpoint_bag_put(user: str, slot_bag: int, slot_pc: int) -> None:
    return None

@app.delete("/bag", tags=["bag"])
async def endpoint_bag_delete(user: str, slot: int) -> None:
    return None