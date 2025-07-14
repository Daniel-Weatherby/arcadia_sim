import csv
import os

class AgentDataLogger:
    def __init__(self, filename="agent_stats.csv"):
        self.filename = filename
        self.headers_written = False
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "day", "agent", "age", "money", "energy", "happiness",
                    "food_need", "health_need", "education_need", "work_need"
                ])
                self.headers_written = True

    def log(self, day, agents):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for agent in agents:
                writer.writerow([
                    day,
                    agent.name,
                    agent.age,
                    round(agent.money, 2),
                    round(agent.energy, 2),
                    round(agent.happiness, 2),
                    round(agent.needs.get("food", 0), 2),
                    round(agent.needs.get("health", 0), 2),
                    round(agent.needs.get("education", 0), 2),
                    round(agent.needs.get("work", 0), 2),
                ])
