from models.agent import Agent
from environment import Environment, Service

# Create the environment and add services
env = Environment()
env.add_service(Service("Wellness Clinic", capacity=2, service_type="physical"))
env.add_service(Service("Security Hub", capacity=1, service_type="safety"))
env.add_service(Service("Community Center", capacity=2, service_type="belonging"))
env.add_service(Service("Job Centre", capacity=2, service_type="purpose"))

# Create agents
agents = [Agent(f"Agent {i}", age=20 + i) for i in range(5)]

# Simulate one day
print("\n🌅 A new day in Arcadia:")
for agent in agents:
    agent.live_one_day(env)

# Print agent status
print("\n📊 Agent Summary:")
for agent in agents:
    print(f"{agent.name}: happiness={agent.happiness:.2f}, energy={agent.energy}, needs={agent.needs}")

# Reset services
env.reset_services()
