import asyncio
from aio_pika import connect, Message, DeliveryMode
import json
class RabbitMQRPCClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}

    async def connect(self):
        if not self.connection:
            self.connection = await connect("amqp://guest:guest@palmon_rabbitmq/")
            self.channel = await self.connection.channel()
            self.callback_queue = await self.channel.declare_queue(exclusive=True)

            async def on_response(message):
                async with message.process():
                    res = json.loads(message.body.decode())
                    self.futures[res["correlation_id"]].set_result(res["res"])
                    del self.futures[res["correlation_id"]]

            await self.callback_queue.consume(on_response, no_ack=False)
        return ""

    async def call(self, queue_name: str, correlation_id, message):
        if not self.connection:
            await self.connect()

        future = asyncio.Future()
        self.futures[correlation_id] = future
        await self.channel.default_exchange.publish(
            Message(
                body=message.encode(),
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=queue_name,
        )
        return await future
