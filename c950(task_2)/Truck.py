from datetime import datetime, timedelta

class Truck:
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, truck_id, capacity=16, speed=18):
        # Initialize a Truck object with given id, capacity, and speed.
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed  # miles per hour
        self.packages = []  # List to store packages
        self.mileage = 0
        self.current_location = "HUB"
        self.departure_time = None
        self.end_time = None

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def load_package(self, package):
        # Load a package onto the truck if there's capacity.
        # Returns True if loaded successfully, False otherwise.
        if len(self.packages) < self.capacity:
            self.packages.append(package)  # O(1) amortized time for append
            return True
        return False

    # Time Complexity: O(n) where n is the number of packages on the truck
    # Space Complexity: O(1)
    def unload_package(self, package):
        # Unload a package from the truck.
        # Returns True if unloaded successfully, False if package not found.
        if package in self.packages:  # O(n) time for 'in' operation
            self.packages.remove(package)  # O(n) time for remove
            return True
        return False

    # Time Complexity: O(n) where n is the number of packages on the truck
    # Space Complexity: O(1)
    def deliver_package(self, package, distance):
        # Deliver a package, update mileage and location.
        # Returns True if delivered successfully, False otherwise.
        if self.unload_package(package):  # O(n) time
            self.mileage += distance
            travel_time = timedelta(hours=distance / self.speed)
            delivery_time = self.departure_time + travel_time
            package.update_status('Delivered', delivery_time)  # Assuming O(1) time
            self.current_location = package.address
            return True
        return False

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def start_delivery(self, start_time):
        """Set the departure time for the truck."""
        self.departure_time = start_time
        self.return_time = None

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def end_delivery(self, end_time):
        """Set the return time for the truck."""
        self.return_time = end_time

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def reset(self):
        """Reset the truck's state."""
        self.packages = []
        self.mileage = 0
        self.current_location = "HUB"
        self.departure_time = None
        self.return_time = None

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def is_full(self):
        # Check if the truck is at full capacity.
        return len(self.packages) >= self.capacity

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def get_current_load(self):
        # Get the current number of packages on the truck.
        return len(self.packages)

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __str__(self):
        #String representation of the truck's status.
        return f"Truck {self.truck_id}: {len(self.packages)}/{self.capacity} packages, {self.mileage} miles"
