from models.agent import Agent
from environment import Environment, Service

# Setup
env = Environment()
env.add_service(Service("Clinic A", 2, "health"))
env.add_service(Service("School A", 2, "education"))

agents = [Agent(f"Agent {i}", age=20 + i) for i in range(4)]

# Simulate a day
for agent in agents:
    agent.act(env)

# Reset services for the next day
env.reset_services()