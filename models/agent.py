class Agent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100
        self.happiness = 1.0
        self.money = 50  # Starting money
        self.needs = {
            "food": 0.0,
            "health": 0.0,
            "education": 0.0,
            "work": 0.0,
        }
        self.alive = True
        self.work_earnings_per_tick = 10  # Earnings for using work service
        self.work_cooldown = 0  # ticks before can work again

    def is_alive(self):
        return self.alive

    def update_energy_and_check_death(self):
        if self.energy <= 0:
            self.alive = False

    def evaluate_needs(self):
        # Needs increase over time
        self.needs["food"] += 0.5
        self.needs["health"] += 0.2
        self.needs["education"] += 0.3
        self.needs["work"] += 0.4

        # Reduce work cooldown if set
        if self.work_cooldown > 0:
            self.work_cooldown -= 1

    def decide_need(self):
        if self.energy <= 25:
            return "food"  # Prioritize food when energy is low
        return max(self.needs, key=self.needs.get)

    def fulfill_need(self, need_type):
        if need_type in self.needs:
            self.needs[need_type] = 0.0

    def earn_money_from_work(self):
        """Called when agent uses work service successfully."""
        if self.work_cooldown == 0:
            self.money += self.work_earnings_per_tick
            self.work_cooldown = 5  # example cooldown to prevent continuous earning

    def can_afford(self, cost):
        """Check if agent has enough money to pay cost."""
        return self.money >= cost

    def pay(self, cost):
        """Deduct cost from money if affordable, else return False."""
        if self.can_afford(cost):
            self.money -= cost
            return True
        return False
