from models.agent import Agent
from environment import Environment, Service

# Setup environment
env = Environment()
env.add_service(Service("Wellness Clinic", 2, "physical"))
env.add_service(Service("Security Hub", 1, "safety"))
env.add_service(Service("Community Center", 2, "belonging"))
env.add_service(Service("Job Centre", 2, "purpose"))
env.add_service(Service("Big Snack Takeaway", capacity=2, service_type="food"))

# Create agents
agents = [Agent(f"Agent {i}", age=20 + i) for i in range(5)]

# Run simulation over multiple days
days = 30
for day in range(1, days + 1):
    print(f"\n🌄 Day {day} in Arcadia:")

    for agent in agents:
        agent.live_one_day(env)

    print("\n📊 Daily Summary:")
    for agent in agents:
        print(f"{agent.name}: happiness={agent.happiness:.2f}, energy={agent.energy}, needs={agent.needs}")

    env.reset_services()
