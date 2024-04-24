import asyncio, aiomqtt


class Subscriber:

    def __init__(self, mqttConfig):
        self.config = mqttConfig
        if not self.mqttClient:
            self.mqttClient = aiomqtt.Client(
                hostname=self.config["host"],
                port=self.config["port"],
                username=self.config["username"],
                password=self.config["password"],
            )

    # async def sleep(self, seconds=1):
    #     await asyncio.sleep(seconds)

    async def subscribe(self, topic):
        async with self.mqttClient as mqttClient:
            await mqttClient.subscribe(topic)
            async for message in mqttClient.messages:
                print(message.payload)
