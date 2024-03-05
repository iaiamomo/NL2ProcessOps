from manufacturer import AssembleInterior, SendRequirements, CreateTestProtocol

class AirplaneManufacturer:
    def __init__(self):
        self.teams = {
            'vodka_bar': 'Russian team',
            'whiskey_bar': 'Irish team',
            # Add other teams as needed
        }

    def produce_airplane(self, specifications: dict):
        # Send requirements to different teams
        for part, team in self.teams.items():
            if part in specifications:
                SendRequirements.call([part])

        # Wait for parts to be manufactured and delivered
        # This can be simulated with a delay or you can implement a real waiting mechanism
        # time.sleep(60)

        # Assemble the interior of the plane
        AssembleInterior.call(specifications['parts'], specifications['product_id'])

        # Send the plane on a test flight and create a test protocol
        test_protocol = CreateTestProtocol.call()

        # Send the test protocol to the manufacturer and the customer
        # send_test_protocol(test_protocol, manufacturer, customer)

        # Deliver the plane to the customer and wait for confirmation
        # deliver_plane(customer)
        # wait_for_confirmation(customer)