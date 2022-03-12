import logging
import uuid
from webthing import ( Action, Property, Thing, Value, WebThingServer, MultipleThings )



class SwitchAction(Action):

    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'on-off', input_)

    def perform_action(self):
        print(f"Performing action on the device: {self.thing.id} on the property: {self.input['propertyId']} with input: {self.input['switch_state']}")
        property_id = self.input['propertyId']
        self.thing.set_property(property_id, self.input['switch_state'])

        # self.thing.notify_of_external_update(property_id)


class VirtualSwitch1CH(Thing):

    def __init__(self, id):

        Thing.__init__(
            self,
            f'SW-1CH-Virtual-{id}',
            'Virtual 1CH Switch',
            ['OnOffProperty', 'OnOffSwitch'],
            'A Qube Virtual 1 Channel Switch',
       )

        self.switch_state_a = Value(True)

        self.add_property(
            Property(
                self,
                'switchA',
                self.switch_state_a,
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
                    'required': ['propertyId', 'switch_state'],
                    'properties': {
                        'propertyId': {
                            'type': 'string',
                        },
                        'switch_state': {
                            'type': 'boolean',
                        }
                    },
                },
            },
            SwitchAction
        )
        print("Switch 1CH initialized")

    def update_swtich_state(self):

        self.switch_state.notify_of_external_update(self.switch_state_a.value)



class VirtualSwitch2CH(Thing):

    def __init__(self, id):

        Thing.__init__(
            self,
            f'SW-2CH-Virtual-{id}',
            'Virtual 2CH Switch',
            ['OnOffProperty', 'OnOffSwitch'],
            'A Qube Virtual 2 Channel Switch',
       )

        self.switch_state_a = Value(True)
        self.switch_state_b = Value(True)

        self.add_property(
            Property(
                self,
                'switchA',
                self.switch_state_a,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchA',
                    'type': 'boolean',
                    'description': 'Whether the switchA is on or off', 
                }
            )
        )

        self.add_property(
            Property(
                self,
                'switchB',
                self.switch_state_b,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchB',
                    'type': 'boolean',
                    'description': 'Whether the switchB is on or off',
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
                    'required': ['propertyId', 'switch_state'],
                    'properties': {
                        'propertyId': {
                            'type': 'string',
                        },
                        'switch_state': {
                            'type': 'boolean',
                        }
                    },
                },
            },
            SwitchAction
        )
        print("Switch 2CH initialized")



class VirtualSwitch4CH(Thing):

    def __init__(self, id):

        Thing.__init__(
            self,
            f'SW-4CH-Virtual-{id}',
            'Virtual 4CH Switch',
            ['OnOffProperty', 'OnOffSwitch'],
            'A Qube Virtual 4 Channel Switch',
       )

        self.switch_state_a = Value(True)
        self.switch_state_b = Value(True)
        self.switch_state_c = Value(True)
        self.switch_state_d = Value(True)


        self.add_property(
            Property(
                self,
                'switchA',
                self.switch_state_a,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchA',
                    'type': 'boolean',
                    'description': 'Whether the switchA is on or off', 
                }
            )
        )

        self.add_property(
            Property(
                self,
                'switchB',
                self.switch_state_b,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchB',
                    'type': 'boolean',
                    'description': 'Whether the switchB is on or off',
                }
            )
        )

        self.add_property(
            Property(
                self,
                'switchC',
                self.switch_state_c,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchC',
                    'type': 'boolean',
                    'description': 'Whether the switchC is on or off', 
                }
            )
        )

        self.add_property(
            Property(
                self,
                'switchD',
                self.switch_state_d,
                metadata={
                    '@type': 'OnOffProperty',
                    'title': 'switchD',
                    'type': 'boolean',
                    'description': 'Whether the switchD is on or off', 
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
                    'required': ['propertyId', 'switch_state'],
                    'properties': {
                        'propertyId': {
                            'type': 'string',
                        },
                        'switch_state': {
                            'type': 'boolean',
                        }
                    },
                },
            },
            SwitchAction
        )
        print("Switch 4CH initialized")



def run_switches():
    thing_1ch = VirtualSwitch1CH(1)
    thing_2ch = VirtualSwitch2CH(1)
    thing_4ch = VirtualSwitch4CH(1)
    things = [thing_1ch, thing_2ch, thing_4ch]

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings(things,'test-switches'), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        logging.info('stopping the server')
        print("Stopping the Switches")
        server.stop()
        logging.info('done')




