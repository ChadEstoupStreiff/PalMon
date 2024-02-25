import asyncio
import json
import logging
from datetime import datetime, timedelta

from aio_pika import IncomingMessage, connect
from db import DB
from objects import Egg, Incubator


def get_eggs(owner: str):
    return DB().get().query(Egg).filter_by(owner=owner).first()


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


async def get_date() -> str:
    return str(datetime.now())


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


async def endpoint_incubator_get(owner: str):
    incubators = get_incubators(owner)
    if len(incubators) == 0:
        create_incubator(owner)
        return get_incubators(owner)
    return incubators


async def endpoint_incubator_create(owner: str) -> bool:
    incubators = get_incubators(owner)
    if incubators is not None and len(incubators) < 6:
        create_incubator(owner)
        return True
    return False


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
        and incubator.hatch_date <= datetime.now()
    ):
        incubator.occupied = False
        incubator.hatch_date = None
        commit.commit()
        return True
    return False


async def on_request(message: IncomingMessage):
    async with message.process():
        logging.info(f"Received request: {message.body.decode()}")
        request = json.loads(message.body.decode())
        response = ""
        message.correlation_id

        if request["path"] == "egg" and request["type"] == "get":
            response = json.dumps(await endpoint_egg_get(request["owner"]))
        if request["path"] == "date" and request["type"] == "get":
            response = str(datetime.now())
        if request["path"] == "egg" and request["type"] == "post":
            response = json.dumps(
                await endpoint_egg_create(request["owner"], request["quantity"])
            )
        if request["path"] == "incubator" and request["type"] == "get":
            response = json.dumps(
                [ob.toJson() for ob in await endpoint_incubator_get(request["owner"])]
            )
        if request["path"] == "incubator" and request["type"] == "post":
            response = json.dumps(await endpoint_incubator_create(request["owner"]))
        if request["path"] == "incubator/place" and request["type"] == "post":
            response = json.dumps(
                await endpoint_incubator_touch(
                    request["owner"],
                    request["incubator_id"],
                )
            )
        if request["path"] == "incubator/hatch" and request["type"] == "post":
            response = json.dumps(
                await endpoint_incubator_hatch(
                    request["owner"], request["incubator_id"]
                )
            )

        await message.channel.basic_publish(
            json.dumps(
                {"correlation_id": message.correlation_id, "res": response}
            ).encode(),
            routing_key=message.reply_to,
        )


async def main():
    connection = await connect("amqp://guest:guest@palmon_rabbitmq/")
    channel = await connection.channel()

    queue = await channel.declare_queue("egg")
    await queue.consume(on_request, no_ack=False)

    logging.info("Awaiting RPC requests")
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    logging.basicConfig(encoding="utf-8", level=logging.INFO)
    asyncio.run(main())
