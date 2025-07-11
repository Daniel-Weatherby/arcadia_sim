import random
from environment import Environment, Service

class Agent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100
        self.happiness = random.uniform(0.4, 0.6)

        # Maslow-style needs state (1 = unmet, 0 = satisfied)
        self.needs = {
            "physical": 1,
            "safety": 1,
            "belonging": 1,
            "purpose": 1,
        }

    def evaluate_needs(self):
        """Simulate changes in needs"""
        for need in self.needs:
            if random.random() < 0.3:
                self.needs[need] = 1  # need arises again
            else:
                self.needs[need] = 0  # currently satisfied

    def act(self, environment):
        """Let the agent try to fulfill one of their needs via the environment.

        Args:
            environment (Environment): The city environment holding services.
        """
        # For now, just hard-code a single need (e.g. 'health')
        need = "health"
        services = environment.get_services_by_type(need)

        for service in services:
            if service.use(self.name):
                print(f"{self.name} used {service.name} for {need}.")
                return  # success — agent is done
        print(f"{self.name} could not find an available {need} service.")

    def live_one_day(self):
        self.evaluate_needs()
        self.act()
