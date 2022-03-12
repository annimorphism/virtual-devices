import logging
import uuid
import time
from webthing import ( Action, Property, Thing, Value, WebThingServer, SingleThing )
import tornado


class SwitchAction(Action):

    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'on-off', input_)

    def perform_action(self):
        print(f"Performing action on the device: {self.thing.id} on the property: {self.name} with input: {self.input}")
        self.thing.set_property(self.name, self.input['switchA'])


class VirtualEnergyMeter(Thing):

    def __init__(self, id):
        self.ref_time = time.time()

        Thing.__init__(
            self,
            f'SU-Virtual-{id}',
            'Virtual Energy Meter',
            ['EnergyMonitor', 'EnergyMeterProperty', 'OnOffProperty', 'PowerProperty'],
            'A Qube Virtual Energy Meter',
       )

        self.energy = Value(0)

        self.power = Value(5000)

        self.meter_state = Value(True)

        self.add_property(
            Property(
                self,
                'energy',
                self.energy,
                metadata={
                    '@type': 'EnergyMeterProperty',
                    'title': 'Energy',
                    'type': 'number',
                    'unit': 'kWh',
                    'description': 'Energy meter reading in kWh',
                    'readOnly': True,
                }
            )
        )

        self.add_property(
            Property(
                self,
                'power',
                self.power,
                metadata={
                    '@type': 'PowerProperty',
                    'title': 'Power',
                    'type': 'number',
                    'unit': 'W',    
                    'description': 'Power reading in W',
                    'readOnly': True,
                }
            )
        )


        self.add_property(
            Property(
                self,
                'switchA',
                self.meter_state,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchA',
                    'type': 'boolean',
                    'description': 'Whether the switch is on or off', 
                }
            )
        )

        self.add_available_action(
            'on-off',
            {
                'title':"On/Off",
                'description': "Turns the switch on or off",
                'input': {
                    'type': 'object',
                    'required': ['switchA'],
                    'properties': {
                        'switchA': {
                            'type': 'boolean',
                        }
                    },
                },
            },
            SwitchAction
        )
        print("Energy Meter initialized")

        self.timer = tornado.ioloop.PeriodicCallback(self.update_energy, 10)
        self.timer.start()

    def update_energy(self):
        new_energy = self.read_energy(self)
        logging.debug(f"New energy: {new_energy}")
        if not self.meter_state.get():
            # This means meter is off, there should be no energy and power reading.
            # self.energy.notify_of_external_update(0)
            self.power.notify_of_external_update(0)
        else:
            self.power.notify_of_external_update(5000)
            self.energy.notify_of_external_update(new_energy)

    def cancel_update_level_task(self):
        self.timer.stop()    


    @staticmethod
    def read_energy(self):
        """Mimic an actual sensor updating its reading every couple seconds."""
        on_time = time.time() - self.ref_time
        new_reading =  ((5000) * (on_time / 60 / 60))/1000
        parsed_reading = round(new_reading, 2)
        return parsed_reading


def run_energy_meter():
    thing = VirtualEnergyMeter(1)

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(SingleThing(thing), port=8889)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        thing.cancel_update_level_task()
        logging.info('stopping the server')
        print("Stopping the Energy Meter")
        server.stop()
        logging.info('done')




