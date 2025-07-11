import random

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

    def act(self):
        """Agent takes action based on most urgent need"""
        for level in ["physical", "safety", "belonging", "purpose"]:
            if self.needs[level] == 1:
                print(f"  {self.name} is trying to satisfy {level} needs.")
                self.energy -= 10
                self.happiness += 0.05  # feels progress
                self.needs[level] = 0   # satisfied for now
                break  # handle one need per day

        self.happiness = max(0, min(1, self.happiness))

    def live_one_day(self):
        self.evaluate_needs()
        self.act()
