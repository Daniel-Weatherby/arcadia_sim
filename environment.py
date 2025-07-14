class Service:
    """Represents a service in the simulation (e.g. school, clinic)."""

    def __init__(self, name, capacity, service_type, x=0, y=0,
                 energy_reward=5, happiness_reward=0.1,
                 usage_duration=3, cost=0):
        self.name = name
        self.capacity = capacity
        self.service_type = service_type
        self.x = x
        self.y = y
        self.energy_reward = energy_reward
        self.happiness_reward = happiness_reward
        self.usage_duration = usage_duration
        self.cost = cost  # New cost attribute
        self.current_users = {}
        self.users_time = {}

    def release(self, agent_name):
        """Remove agent from current users and usage tracking."""
        if agent_name in self.current_users:
            del self.current_users[agent_name]
        if agent_name in self.users_time:
            del self.users_time[agent_name]

    def is_available(self):
        """Return True if service has capacity."""
        return len(self.current_users) < self.capacity

    def use(self, agent):
        """
        Try to let an agent use the service if there's room and agent can pay.
        
        Args:
            agent (Agent): The agent object trying to use the service.

        Returns:
            bool: True if agent started using service, False if not.
        """
        if self.is_available():
            if agent.money >= self.cost:
                agent.money -= self.cost
                self.current_users[agent.name] = self.usage_duration
                self.users_time[agent.name] = self.usage_duration
                return True
            else:
                # Agent cannot afford the service
                return False
        return False

    def tick(self):
        """Advance time: reduce duration for users, remove when done."""
        finished = [a for a, t in self.current_users.items() if t <= 1]
        for agent in finished:
            del self.current_users[agent]
            del self.users_time[agent]
        for agent in self.current_users:
            self.current_users[agent] -= 1
            self.users_time[agent] -= 1

    def reset(self):
        """Clear users — used during full resets."""
        self.current_users.clear()
        self.users_time.clear()


class Environment:
    """Holds all services and manages their state."""

    def __init__(self):
        self.services = {}

    def add_service(self, service):
        """Add a service to the environment."""
        self.services[service.name] = service

    def get_services_by_type(self, service_type):
        """Get all services matching a type."""
        return [s for s in self.services.values() if s.service_type == service_type]

    def reset_services(self):
        """Reset all services (clears users)."""
        for service in self.services.values():
            service.reset()

    def tick_services(self):
        """Simulate passage of one tick in time."""
        for service in self.services.values():
            service.tick()

    def tick(self):
        """Call tick() on all services to update usage timers."""
        for service in self.services.values():
            service.tick()
