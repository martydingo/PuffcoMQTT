from PuffcoPeak.puffcopeak import PuffcoPeak
from .mqtt.subscriber import Subscriber
from .mqtt.publisher import Publisher
import asyncio
import yaml


class PuffcoMQTT:
    def __init__(self, configPath) -> None:
        self.config = self.__loadConfig__(configPath)
        self.mqtt = Publisher(self.config["mqtt"])
        asyncio.run(self.__entrypoint__())

    def __restart__(self):
        asyncio.run(self.__entrypoint__())

    async def __entrypoint__(self):

        self.puffco = await PuffcoPeak(
            self.config["puffco_peak"]["address"],
        )

        # self.mqtt = Publisher(self.config["mqtt"])

        async with asyncio.TaskGroup() as taskGroup:
            # taskGroup.create_task(self.mqtt.subscribe("climate/office/temperature"))
            taskGroup.create_task(self.pollPuffco())

    async def pollPuffcoProfiles(self):
        profiles = [{}, {}, {}, {}]
        for i in range(0, 4):
            profileColor = await self.puffco.get_profile_color(i)
            profiles[i] = {
                "name": await self.puffco.get_profile_name(i),
                "temp": await self.puffco.get_profile_temp(i),
                "time": await self.puffco.get_profile_time(i),
                "color": (
                    profileColor[0],
                    profileColor[1],
                    profileColor[2],
                ),
            }
        return profiles

    async def pollPuffco(self):

        while self.puffco.is_connected:

            current_profile = await self.puffco.get_profile()
            all_profiles = await self.pollPuffcoProfiles()
            print(all_profiles)
            # bowl_temperature = await self.puffco.get_bowl_temperature(celsius=True)

            # curProfile = await self.puffco.get_profile()
            # puffcoData = {
            #     "battery_charge_eta": await self.puffco.get_battery_charge_eta(),
            #     "battery_percentage": await self.puffco.get_battery_percentage(),
            #     # "boost_settings": await self.puffco.get_boost_settings(),
            #     "bowl_temperature": await self.puffco.get_bowl_temperature(
            #         celsius=True
            #     ),
            #     "bluetooth_address": self.puffco.address,
            #     "current_profile": curProfile,
            #     # "current_profile_color": await self.puffco.get_profile_color(
            #     #     curProfile
            #     # ),
            #     "current_profile_name": await self.puffco.get_profile_name(curProfile),
            #     "current_profile_temp": await self.puffco.get_profile_temp(curProfile),
            #     "current_profile_time": await self.puffco.get_profile_time(curProfile),
            #     "daily_dab_count": await self.puffco.get_daily_dab_count(),
            #     "device_birthday": await self.puffco.get_device_birthday(),
            #     # "device_model": await self.puffco.get_device_model(),
            #     "device_name": await self.puffco.get_device_name(),
            #     "lantern_brightness": await self.puffco.get_lantern_brightness(),
            #     # "lantern_color": await self.puffco.get_lantern_color(),
            #     "operating_state": await self.puffco.get_operating_state(),
            #     "state_etime": await self.puffco.get_state_etime(),
            #     "state_ttime": await self.puffco.get_state_ttime(),
            #     "stealth_mode": await self.puffco.get_stealth_mode(),
            #     "target_temp": await self.puffco.get_target_temp(),
            #     "total_dab_count": await self.puffco.get_total_dab_count(),
            #     "is_charging": await self.puffco.is_currently_charging(),
            # }
            # print(puffcoData)
            # device_name = puffcoData["device_name"]
            # for key, value in puffcoData.items():
            #     await self.mqtt.publish(f"puffco/{device_name}/{key}", str(value))

            await asyncio.sleep(self.config["puffco_peak"]["poller"]["interval"])

        self.__restart__()

    def __loadConfig__(self, configPath: str) -> None:
        with open(configPath, "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader)
