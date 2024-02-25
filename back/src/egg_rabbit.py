import json
from uuid import uuid4

import requests
from fastapi import APIRouter
from rabbitmq import RabbitMQRPCClient

rabbitmq_rpc_client = RabbitMQRPCClient()

router = APIRouter(tags=["Egg service"])


@router.get("/egg")
async def endpoint_egg_get(user) -> int:
    correlation_id = str(uuid4())
    response = await rabbitmq_rpc_client.call(
        "egg", correlation_id, json.dumps({"path": "egg", "type": "get", "owner": user})
    )
    return json.loads(response)


@router.get("/date")
async def get_date() -> str:
    correlation_id = str(uuid4())
    response = await rabbitmq_rpc_client.call(
        "egg", correlation_id, json.dumps({"path": "date", "type": "get"})
    )
    return response


@router.get("/incubator")
async def endpoint_incubator_get(user: str):
    correlation_id = str(uuid4())
    response = await rabbitmq_rpc_client.call(
        "egg",
        correlation_id,
        json.dumps({"path": "incubator", "type": "get", "owner": user}),
    )
    return json.loads(response)


@router.post("/incubator/place")
async def endpoint_incubator_touch(user: str, incubator_id: int) -> bool:
    correlation_id = str(uuid4())
    response = await rabbitmq_rpc_client.call(
        "egg",
        correlation_id,
        json.dumps(
            {
                "path": "incubator/place",
                "type": "post",
                "owner": user,
                "incubator_id": incubator_id,
            }
        ),
    )
    return json.loads(response)


@router.post("/incubator/hatch")
async def endpoint_incubator_hatch(user: str, incubator_id: int):
    correlation_id = str(uuid4())
    response = await rabbitmq_rpc_client.call(
        "egg",
        correlation_id,
        json.dumps(
            {
                "path": "incubator/hatch",
                "type": "post",
                "owner": user,
                "incubator_id": incubator_id,
            }
        ),
    )
    if json.loads(response):
        return requests.post("http://palmon_service_palmons:80/palmon").json()
    return False
