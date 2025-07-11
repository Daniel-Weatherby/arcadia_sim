from models.agent import Agent

def run_simulation():
    agents = [
        Agent("Kylie", 12),
        Agent("Mark", 35),
        Agent("Aunty Joan", 55),
    ]

    for day in range(1, 6):
        print(f"\n📅 Day {day}")
        for agent in agents:
            print(f"{agent.name} (happiness: {agent.happiness:.2f})")
            agent.live_one_day()

if __name__ == "__main__":
    run_simulation()
