import logging
import time
from webthing import ( Property, Thing, Value, WebThingServer, SingleThing )
import tornado

class VirtualOccupancySensor(Thing):

    def __init__(self, id):
        self.ref_time = time.time()

        Thing.__init__(
            self,
            f'SE-virtual-{id}',
            'Virtual Occupancy Sensor',
            ['OccupancySensor', 'OccupancySensorProperty', 'OccupancyProperty'],
            'A Qube Virtual Occupancy Sensor',
       )

        self.occupancy_state = Value(False)

        self.add_property(
            Property(
                self,
                'occupancy',
                self.occupancy_state,
                metadata={
                    '@type': 'OccupancyProperty',
                    'title': 'Occupancy',
                    'type': 'boolean',
                    'description': 'Occupancy State of the room',
                    'readOnly': True,
                }
            )
        )

        
        print("Occupancy Sensor initialized")

        self.timer = tornado.ioloop.PeriodicCallback(self.update_occupancy, 5000)
        self.timer.start()

    def update_occupancy(self):
        new_occupancy = self.read_occupancy(self)
        logging.debug(f"New energy: {new_occupancy}")
        self.occupancy_state.notify_of_external_update(new_occupancy)

    def cancel_update_level_task(self):
        self.timer.stop()    


    @staticmethod
    def read_occupancy(self):
        """Mimic an actual sensor updating its reading every couple seconds.
            i.e. Occupancy in the room in every 5 seconds
        """
        if (self.occupancy_state.get()):
            return False
        else:
            return True


def run_occupancy():
    thing = VirtualOccupancySensor(1)

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(SingleThing(thing), port=8887)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        thing.cancel_update_level_task()
        logging.info('stopping the server')
        print("Stopping the Occupancy Sensor")
        server.stop()
        logging.info('done')




