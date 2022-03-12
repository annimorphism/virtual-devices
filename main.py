from http import server
from tkinter import W
from energy_meter import VirtualEnergyMeter
from switches import VirtualSwitch1CH,  VirtualSwitch2CH, VirtualSwitch4CH
from occupancy_sensor import VirtualOccupancySensor
from webthing import (WebThingServer, MultipleThings)

print("This is the Main Application, which when ran will ask you to tell no. of devices to be created i.e. switches, energy-meters, occupancy-meters");

def run_virtual_devices():
    switch_1ch = VirtualSwitch1CH(1)
    switch_2ch = VirtualSwitch2CH(1)
    switch_4ch = VirtualSwitch4CH(1)

    energy_meter = VirtualEnergyMeter(1)

    occupancy_sensor = VirtualOccupancySensor(1)

    things = [switch_1ch, switch_2ch, switch_4ch, energy_meter, occupancy_sensor]

    server = WebThingServer(MultipleThings(things,'virtual-devices'), port=8888)

    try:
        print("starting the Virtual Device server")
        server.start()

    except KeyboardInterrupt:
        print("\nExiting...")
        energy_meter.cancel_update_level_task()

        occupancy_sensor.cancel_update_level_task()

        server.stop()
        exit()

run_virtual_devices()

