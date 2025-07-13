class Service:
    """Represents a service in the simulation (e.g. school, clinic)."""

    def __init__(self, name, capacity, service_type, x=0, y=0, energy_reward=5, happiness_reward=0.1, usage_duration=3):
        self.name = name
        self.capacity = capacity
        self.service_type = service_type
        self.x = x
        self.y = y
        self.energy_reward = energy_reward
        self.happiness_reward = happiness_reward
        self.usage_duration = usage_duration  # new attribute
        self.current_users = {}
        self.users_time = {}  # track time each user has been using the service

    def release(self, agent_name):
        """Remove agent from current users and usage tracking.

        Args:
            agent_name (str): The name of the agent leaving the service.
        """
        if agent_name in self.current_users:
            self.current_users.remove(agent_name)
        if agent_name in self.users_time:
            del self.users_time[agent_name]

    def tick(self):
        """Reduce usage timers and free agents who completed their service."""
        to_remove = []
        for agent_name in self.users_time:
            self.users_time[agent_name] -= 1
            if self.users_time[agent_name] <= 0:
                to_remove.append(agent_name)
        for agent_name in to_remove:
            self.current_users.remove(agent_name)
            del self.users_time[agent_name]

    def is_available(self):
        """Return True if service has capacity."""
        return len(self.current_users) < self.capacity

    def use(self, agent_name):
        """Try to let an agent use the service if there's room."""
        if self.is_available():
            self.current_users[agent_name] = self.usage_duration
            self.users_time[agent_name] = self.usage_duration  # track usage time
            return True
        return False

    def tick(self):
        """Advance time: reduce duration for users, remove when done."""
        finished = [a for a, t in self.current_users.items() if t <= 1]
        for agent in finished:
            del self.current_users[agent]
        for agent in self.current_users:
            self.current_users[agent] -= 1

    def reset(self):
        """Clear users — used during full resets."""
        self.current_users.clear()


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