import asyncio, aiomqtt, json


class Publisher:
    def __init__(self, mqttConfig):
        self.config = mqttConfig
        self.mqttClient = None

    async def publish(self, topic, payload):
        if not self.mqttClient:
            self.mqttClient = aiomqtt.Client(
                hostname=self.config["host"],
                port=self.config["port"],
                username=self.config["username"],
                password=self.config["password"],
            )

        async with self.mqttClient as mqttClient:
            await mqttClient.publish(topic, payload)
            await self.publish_to_homeassistant_discover(topic, mqttClient)

    async def publish_to_homeassistant_discover(self, topic, mqttClient):
        key = topic.split("/")[-1]
        device_name = topic.split("/")[-2]

        if not self.mqttClient:
            self.mqttClient = aiomqtt.Client(
                hostname=self.config["host"],
                port=self.config["port"],
                username=self.config["username"],
                password=self.config["password"],
            )

        unit = ""
        device_class = ""
        if "temp" in key:
            unit = "°C"
        elif "battery_percentage" in key:
            unit = "%"
            device_class = "battery"

        discoveryPayload = {
            "name": f"{key}",
            "state_topic": topic,
            "unit_of_measurement": unit,
            "device_class": device_class,
            "unique_id": f"{device_name.replace(' ', '_')}_{key}",
            "device": {
                "identifiers": [device_name],
                "name": device_name,
                "model": "Peak Pro",
                "manufacturer": "Puffco",
            },
        }

        await mqttClient.publish(
            f"homeassistant/sensor/{device_name.replace(' ', '_')}/{key}/config",
            json.dumps(discoveryPayload),
        )
