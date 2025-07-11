class Service:
    """Represents a service in the simulation (e.g. school, clinic)."""

    def __init__(self, name, capacity, service_type):
        """Initialize a new service.

        Args:
            name (str): The name of the service (e.g. 'Clinic A').
            capacity (int): Maximum number of people it can serve at once.
            service_type (str): What need this service satisfies ('health', 'education', etc.).
        """
        self.name = name
        self.capacity = capacity
        self.service_type = service_type
        self.current_users = []

    def is_available(self):
        """Check if the service has room for more users.

        Returns:
            bool: True if the service is not full, False otherwise.
        """
        return len(self.current_users) < self.capacity
    
    def use(self, agent):
        """Try to let an agent use the service if there's room.

        Args:
            agent (any): The agent trying to use the service.

        Returns:
            bool: True if the agent was added, False if service is full.
        """
        if self.is_available():
            self.current_users.append(agent)
            return True
        return False

    def reset(self):
        """Reset the service by clearing the list of current users."""
        self.current_users.clear()


class Environment:
    """Represents the city environment containing community services.

    Attributes:
        services (dict): Maps service name (str) to Service instances.
    """

    def __init__(self):
        """Initialize an empty environment with no services."""
        self.services = {}
    
    def add_service(self, service):
        """Add a Service object to the environment.

        Args:
            service (Service): A Service instance to add.
        """
        self.services[service.name] = service

    def get_services_by_type(self, service_type):
        """Return a list of services matching the given type.

        Args:
            service_type (str): The type of service (e.g. 'health').

        Returns:
            list: List of Service objects matching the type.
        """
        return [s for s in self.services.values() if s.service_type == service_type]

    def reset_services(self):
        """Call reset() on all services to clear their current users."""
        for service in self.services.values():
            service.reset()



if __name__ == "__main__":
    # Existing tests for Service...

    # Environment tests
    env = Environment()
    env.add_service(Service("Clinic A", 2, "health"))
    env.add_service(Service("School A", 10, "education"))

    health_services = env.get_services_by_type("health")
    print(f"Health services: {[s.name for s in health_services]}")  # ['Clinic A']

    env.services["Clinic A"].use("Agent1")
    env.services["Clinic A"].use("Agent2")
    print(env.services["Clinic A"].is_available())  # False

    env.reset_services()
    print(env.services["Clinic A"].current_users)  # []
