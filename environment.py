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



if __name__ == "__main__":
    clinic = Service("Clinic A", capacity=2, service_type="health")

    clinic.use("Agent1")
    clinic.use("Agent2")
    print(clinic.current_users)  # ['Agent1', 'Agent2']

    clinic.reset()
    print(clinic.current_users)  # []
