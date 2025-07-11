from models.agent import Agent
from environment import Environment, Service

# Create environment and services
env = Environment()
env.add_service(Service("Clinic A", capacity=2, service_type="health"))

# Create agents
agents = [Agent(f"Agent {i}", age=25 + i) for i in range(3)]

# Simulate one day
for agent in agents:
    agent.act(env)

# Reset for the next day
env.reset_services()

