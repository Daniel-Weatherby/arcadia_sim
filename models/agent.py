import random

class Agent:
    """Represents a person in the simulation with needs and decision-making."""

    def __init__(self, name, age):
        """
        Initialize the agent with a name, age, and base needs.

        Args:
            name (str): The name of the agent.
            age (int): Age of the agent.
        """
        self.name = name
        self.age = age
        self.energy = 100
        self.happiness = random.uniform(0.4, 0.6)

        # Needs: values from 0.0 (satisfied) to 1.0 (critical)
        self.needs = {
            "food": random.uniform(0.2, 0.6),
            "health": random.uniform(0.2, 0.6),
            "education": random.uniform(0.2, 0.6)
        }

    def evaluate_needs(self):
        """Adjust needs over time — increase or decay them based on state."""
        for need, level in self.needs.items():
            # If satisfied (low), decay a bit
            if level < 0.5:
                decay = random.uniform(0.01, 0.05)
                self.needs[need] = max(0.0, level - decay)
            else:
                # If unmet (high), increase further
                increase = random.uniform(0.05, 0.1)
                self.needs[need] = min(1.0, level + increase)

    def decide_need(self):
        """Choose the most urgent need."""
        most_urgent = max(self.needs.items(), key=lambda item: item[1])
        print(f"{self.name} choosing {most_urgent[0]} (urgency: {most_urgent[1]:.2f})")
        return most_urgent[0]

    def fulfill_need(self, need):
        """Lower the urgency of a need after using a service.

        Args:
            need (str): The need being fulfilled.
        """
        if need in self.needs:
            self.needs[need] = max(0.0, self.needs[need] - 0.8)

    def get_need_level(self, need):
        """Return the urgency level of a given need."""
        return self.needs.get(need, 0.0)
