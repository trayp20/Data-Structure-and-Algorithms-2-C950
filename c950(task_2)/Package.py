class Package:
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, id, address, city, state, zip_code, deadline, weight, notes=''):
        # Initialize a Package object with given attributes.
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = 'At hub'
        self.delivery_time = None
        self.delivery_truck = None 
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __str__(self):
        # Return a string representation of the package.
        return f"Package {self.id}: {self.address}, {self.city}, {self.state} {self.zip_code}"

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def update_status(self, status, delivery_time=None):
        # Update the status of the package and optionally set the delivery time.
        self.status = status
        if delivery_time:
            self.delivery_time = delivery_time

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def get_status(self, current_time):
        # Get the current status of the package based on the given time.
        if self.delivery_time:
            if current_time >= self.delivery_time:
                return f"Delivered at {self.delivery_time.strftime('%H:%M:%S')}"
            else:
                return "En route"
        elif self.status == 'At hub':
            return "At hub"
        else:
            return self.status

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def is_delayed(self):
        # Check if the package is delayed based on its notes.
        return "Delayed" in self.notes

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def can_be_on_truck(self, truck_number):
        # Check if the package can be loaded on a specific truck.
        if "Can only be on truck 2" in self.notes:
            return truck_number == 2
        return True
