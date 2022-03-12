from energy_meter import VirtualEnergyMeter
from switches import VirtualSwitch1CH,  VirtualSwitch2CH, VirtualSwitch4CH
from occupancy_sensor import VirtualOccupancySensor
from webthing import (WebThingServer, MultipleThings)

print("This is the Main Application, which will create 1 virtual device of each Switch-1CH, Switch-2CH, Switch-4CH, Energy-Meter, Occupancy-Sensor\n");

def run_virtual_devices():
    switch_1ch = VirtualSwitch1CH(1)
    switch_2ch = VirtualSwitch2CH(1)
    switch_4ch = VirtualSwitch4CH(1)

    energy_meter = VirtualEnergyMeter(1)

    occupancy_sensor = VirtualOccupancySensor(1)

    things = [switch_1ch, switch_2ch, switch_4ch, energy_meter, occupancy_sensor]

    server = WebThingServer(MultipleThings(things,'virtual-devices'), hostname='0.0.0.0', port=5000)

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

