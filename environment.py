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

if __name__ == "__main__":
    clinic = Service("Clinic A", 5, "health")
    print(f"Service: {clinic.name}, Type: {clinic.service_type}, Capacity: {clinic.capacity}")