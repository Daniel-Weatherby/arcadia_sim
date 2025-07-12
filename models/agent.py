import random
from environment import Environment, Service

class Agent:
    """Represents a person in the Arcadia simulation."""

    def __init__(self, name, age):
        """Initialize an agent with basic attributes and unmet needs."""
        self.name = name
        self.age = age
        self.energy = 100
        self.happiness = random.uniform(0.4, 0.6)

        # Maslow-style needs: 1 = unmet, 0 = satisfied
        self.needs = {
            "physical": 1,
            "safety": 1,
            "belonging": 1,
            "purpose": 1,
        }

    def decide_need(self):
        """Decide the most urgent unmet need.

        Returns:
            str or None: The name of the most pressing unmet need.
        """
        for need, state in self.needs.items():
            if state == 1:
                return need
        return None  # All needs are currently satisfied

    def evaluate_needs(self):
        """Randomly reintroduce needs each day."""
        for need in self.needs:
            if random.random() < 0.3:
                self.needs[need] = 1  # need arises
            else:
                self.needs[need] = 0  # currently satisfied

    def act(self, environment):
        """Let the agent try to fulfill one of their needs.

        Args:
            environment (Environment): The environment with services.
        """
        need = self.decide_need()
        if not need:
            print(f"{self.name} has no pressing needs today.")
            return

        services = environment.get_services_by_type(need)

        for service in services:
            if service.use(self.name):
                self.needs[need] = 0  # mark need as satisfied
                self.happiness = min(1.0, self.happiness + 0.05)
                self.energy -= 5
                print(f"{self.name} fulfilled {need} at {service.name}. 😊")
                return

        # If no service was available
        self.happiness = max(0.0, self.happiness - 0.05)
        self.energy -= 10
        print(f"{self.name} failed to fulfill {need}. 😞")

    def live_one_day(self, environment):
        """Simulate a full day: evaluate needs and act."""
        self.evaluate_needs()
        self.act(environment)
