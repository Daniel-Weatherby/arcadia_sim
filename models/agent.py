import random
from environment import Environment, Service

class Agent:
    """Represents a person in the Arcadia simulation."""

    def __init__(self, name, age):
        """Initialize an agent with basic attributes and unmet needs.

        Args:
            name (str): The agent's name.
            age (int): The agent's age.
        """
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
            "food": 1  # special logic
        }

    def decide_need(self):
        """Decide which need to try fulfilling today.

        Returns:
            str or None: The most pressing unmet need.
        """
        if self.energy < 50 and self.needs.get("food", 0) == 1:
            return "food"

        for need, state in self.needs.items():
            if state == 1:
                return need

        return None  # All needs satisfied

    def evaluate_needs(self):
        """Randomly reactivate needs to simulate life pressure."""
        for need in self.needs:
            if random.random() < 0.3:
                self.needs[need] = 1
            else:
                self.needs[need] = 0

    def act(self, environment):
        """Try to fulfill one need based on environment.

        Args:
            environment (Environment): The environment of available services.
        """
        need = self.decide_need()
        if not need:
            print(f"{self.name} has no pressing needs today.")
            return

        # Special logic for food
        if need == "food":
            if self.energy < 50:
                services = environment.get_services_by_type("food")
                for service in services:
                    if service.use(self.name):
                        self.energy = min(100, self.energy + 5)
                        self.happiness = min(1.0, self.happiness + 0.2)
                        self.needs["food"] = 0
                        print(f"{self.name} got takeaway from {service.name}. 🍔")
                        return
                print(f"{self.name} wanted takeaway but it wasn't available. 😞")
            else:
                self.energy = min(100, self.energy + 3)
                self.happiness = min(1.0, self.happiness + 0.1)
                self.needs["food"] = 0
                print(f"{self.name} ate at home. 🍽️")
            return

        # Handle regular needs
        services = environment.get_services_by_type(need)
        for service in services:
            if service.use(self.name):
                self.needs[need] = 0
                self.happiness = min(1.0, self.happiness + 0.05)
                self.energy -= 5
                print(f"{self.name} fulfilled {need} at {service.name}. 😊")
                return

        # If no service was available
        self.happiness = max(0.0, self.happiness - 0.05)
        self.energy -= 10
        print(f"{self.name} failed to fulfill {need}. 😞")

    def live_one_day(self, environment):
        """Run a full simulation tick for this agent.

        Args:
            environment (Environment): The town services.
        """
        self.evaluate_needs()
        self.act(environment)
        self.energy = max(0, self.energy - 2)  # passive fatigue
