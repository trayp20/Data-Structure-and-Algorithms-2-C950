#Author Trayvonious Pendleton'
#studentID 011205284

import csv
from datetime import datetime, timedelta
from HashTable import HashTable
from Package import Package
from Truck import Truck


# Global constants
TRUCK_CAPACITY = 16
TRUCK_SPEED = 18  # mph
START_TIME = datetime.strptime("08:00:00", "%H:%M:%S")
HUB_ADDRESS = "4001 South 700 East"

# Time Complexity: O(n), where n is the number of packages in the CSV file
# Space Complexity: O(n) for storing all packages in the hash table
def load_package_data(filename):
    """ Load package data from CSV file into a hash table.
    
    Why: Efficient data storage and retrieval are crucial for the package delivery system.
    What: This function reads package data from a CSV file and stores it in a hash table.
    How: 
    1. Initialize a HashTable with a capacity of 40.
    2. Open and read the CSV file, skipping header rows.
    3. For each valid row, create a Package object and insert it into the hash table.
    4. Handle special cases like delayed packages by setting their available time.
    """
    packages = HashTable(40)
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Skip header rows
        for _ in range(5):
            next(reader)
        for row in reader:
            if len(row) >= 8 and row[0].strip().isdigit():
                try:
                    id = int(row[0])
                    package = Package(
                        id=id,
                        address=row[1],
                        city=row[2],
                        state=row[3],
                        zip_code=row[4],
                        deadline=row[5],
                        weight=float(row[6]),
                        notes=row[7] if len(row) > 7 else ''
                    )
                    if "Delayed" in package.notes:
                        package.available_time = datetime.strptime("09:05:00", "%H:%M:%S")
                    else:
                        package.available_time = START_TIME
                    packages.insert(id, package)
                except ValueError as e:
                    print(f"Error processing row {row}: {e}")
    return packages

# Time Complexity: O(1) - constant time as it returns a predefined matrix
# Space Complexity: O(m^2) where m is the number of addresses
def create_distance_matrix():
    """Create distance matrix manually."""
    # Returns a predefined 2D list representing distances between locations
    return [
        [0, 7.2, 3.8, 11.0, 2.2, 3.5, 10.9, 8.6, 7.6, 2.8, 6.4, 3.2, 7.6, 5.2, 4.4, 3.7, 7.6, 2.0, 3.6, 6.5, 1.9, 3.4, 2.4, 6.4, 2.4, 5.0, 3.6],
        [7.2, 0, 7.1, 6.4, 6.0, 4.8, 1.6, 2.8, 4.8, 6.3, 7.3, 5.3, 4.8, 3.0, 4.6, 4.5, 7.4, 6.0, 5.0, 4.8, 9.5, 10.9, 8.3, 6.9, 10.0, 4.4, 13.0],
        [3.8, 7.1, 0, 9.2, 4.4, 2.8, 8.6, 6.3, 5.3, 1.6, 10.4, 3.0, 5.3, 6.5, 5.6, 5.8, 5.7, 4.1, 3.6, 4.3, 3.3, 5.0, 6.1, 9.7, 6.1, 2.8, 7.4],
        [11.0, 6.4, 9.2, 0, 5.6, 6.9, 8.6, 4.0, 11.1, 7.3, 1.0, 6.4, 11.1, 3.9, 4.3, 4.4, 7.2, 5.3, 6.0, 10.6, 5.9, 7.4, 4.7, 0.6, 6.4, 10.1, 10.1],
        [2.2, 6.0, 4.4, 5.6, 0, 1.9, 7.9, 5.1, 7.5, 2.6, 6.5, 1.5, 7.5, 3.2, 2.4, 2.7, 1.4, 0.5, 1.7, 6.5, 3.2, 5.2, 2.5, 6.0, 4.2, 5.4, 5.5],
        [3.5, 4.8, 2.8, 6.9, 1.9, 0, 6.3, 4.3, 4.5, 1.5, 8.7, 0.8, 4.5, 3.9, 3.0, 3.8, 5.7, 1.9, 1.1, 3.5, 4.9, 6.9, 4.2, 9.0, 5.9, 3.5, 7.2],
        [10.9, 1.6, 8.6, 8.6, 7.9, 6.3, 0, 4.0, 4.2, 8.0, 8.6, 6.9, 4.2, 4.2, 8.0, 5.8, 7.2, 7.7, 6.6, 3.2, 11.2, 12.7, 10.0, 8.2, 11.7, 5.1, 14.2],
        [8.6, 2.8, 6.3, 4.0, 5.1, 4.3, 4.0, 0, 7.7, 9.3, 4.6, 4.8, 7.7, 1.6, 3.3, 3.4, 3.1, 5.1, 4.6, 6.7, 8.1, 10.4, 7.8, 4.2, 9.5, 6.2, 10.7],
        [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0, 4.8, 11.9, 4.7, 0.6, 7.6, 7.8, 6.6, 7.2, 5.9, 5.4, 1.0, 8.5, 10.3, 7.8, 11.5, 9.5, 2.8, 14.1],
        [2.8, 6.3, 1.6, 7.3, 2.6, 1.5, 8.0, 9.3, 4.8, 0, 9.4, 1.1, 5.1, 4.6, 3.7, 4.0, 6.7, 2.3, 1.8, 4.1, 3.8, 5.8, 4.3, 7.8, 4.8, 3.2, 6.0],
        [6.4, 7.3, 10.4, 1.0, 6.5, 8.7, 8.6, 4.6, 11.9, 9.4, 0, 7.3, 12.0, 4.9, 5.2, 5.4, 8.1, 6.2, 6.9, 11.5, 6.9, 8.3, 4.1, 0.4, 4.9, 11.0, 6.8],
        [3.2, 5.3, 3.0, 6.4, 1.5, 0.8, 6.9, 4.8, 4.7, 1.1, 7.3, 0, 4.7, 3.5, 2.6, 2.9, 6.3, 1.2, 1.0, 3.7, 4.1, 6.2, 3.4, 6.9, 5.2, 3.7, 6.4],
        [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0.6, 5.1, 12.0, 4.7, 0, 7.3, 7.8, 6.6, 7.2, 5.9, 5.4, 1.0, 8.5, 10.3, 7.8, 11.5, 9.5, 2.8, 14.1],
        [5.2, 3.0, 6.5, 3.9, 3.2, 3.9, 4.2, 1.6, 7.6, 4.6, 4.9, 3.5, 7.3, 0, 1.3, 1.5, 4.0, 3.2, 3.0, 6.9, 6.2, 8.2, 5.5, 4.4, 7.2, 6.4, 10.5],
        [4.4, 4.6, 5.6, 4.3, 2.4, 3.0, 8.0, 3.3, 7.8, 3.7, 5.2, 2.6, 7.8, 1.3, 0, 0.6, 6.4, 2.4, 2.2, 6.8, 5.3, 7.4, 4.6, 4.8, 6.3, 6.5, 8.8],
        [3.7, 4.5, 5.8, 4.4, 2.7, 3.8, 5.8, 3.4, 6.6, 4.0, 5.4, 2.9, 6.6, 1.5, 0.6, 0, 5.6, 1.6, 1.7, 6.4, 4.9, 6.9, 4.2, 5.6, 5.9, 5.7, 8.4],
        [7.6, 7.4, 5.7, 7.2, 1.4, 5.7, 7.2, 3.1, 7.2, 6.7, 8.1, 6.3, 7.2, 4.0, 6.4, 5.6, 0, 7.1, 6.1, 7.2, 10.6, 12.0, 9.4, 7.5, 11.1, 6.2, 13.6],
        [2.0, 6.0, 4.1, 5.3, 0.5, 1.9, 7.7, 5.1, 5.9, 2.3, 6.2, 1.2, 5.9, 3.2, 2.4, 1.6, 7.1, 0, 1.6, 4.9, 3.0, 5.0, 2.3, 5.5, 4.0, 5.1, 5.2],
        [3.6, 5.0, 3.6, 6.0, 1.7, 1.1, 6.6, 4.6, 5.4, 1.8, 6.9, 1.0, 5.4, 3.0, 2.2, 1.7, 6.1, 1.6, 0, 4.4, 4.6, 6.6, 3.9, 6.5, 5.6, 4.3, 6.9],
        [6.5, 4.8, 4.3, 10.6, 6.5, 3.5, 3.2, 6.7, 1.0, 4.1, 11.5, 3.7, 1.0, 6.9, 6.8, 6.4, 7.2, 4.9, 4.4, 0, 7.5, 9.3, 6.8, 11.4, 8.5, 1.8, 13.1],
        [1.9, 9.5, 3.3, 5.9, 3.2, 4.9, 11.2, 8.1, 8.5, 3.8, 6.9, 4.1, 8.5, 6.2, 5.3, 4.9, 10.6, 3.0, 4.6, 7.5, 0, 2.0, 2.9, 6.4, 2.8, 6.0, 4.1],
        [3.4, 10.9, 5.0, 7.4, 5.2, 6.9, 12.7, 10.4, 10.3, 5.8, 8.3, 6.2, 10.3, 8.2, 7.4, 6.9, 12.0, 5.0, 6.6, 9.3, 2.0, 0, 4.4, 7.9, 3.4, 7.9, 4.7],
        [2.4, 8.3, 6.1, 4.7, 2.5, 4.2, 10.0, 7.8, 7.8, 4.3, 4.1, 3.4, 7.8, 5.5, 4.6, 4.2, 9.4, 2.3, 3.9, 6.8, 2.9, 4.4, 0, 4.5, 1.7, 6.8, 3.1],
        [6.4, 6.9, 9.7, 0.6, 6.0, 9.0, 8.2, 4.2, 11.5, 7.8, 0.4, 6.9, 11.5, 4.4, 4.8, 5.6, 7.5, 5.5, 6.5, 11.4, 6.4, 7.9, 4.5, 0, 5.4, 10.6, 7.8],
        [2.4, 10.0, 6.1, 6.4, 4.2, 5.9, 11.7, 9.5, 9.5, 4.8, 4.9, 5.2, 9.5, 7.2, 6.3, 5.9, 11.1, 4.0, 5.6, 8.5, 2.8, 3.4, 1.7, 5.4, 0, 7.0, 1.3],
        [5.0, 4.4, 2.8, 10.1, 5.4, 3.5, 5.1, 6.2, 2.8, 3.2, 11.0, 3.7, 2.8, 6.4, 6.5, 5.7, 6.2, 5.1, 4.3, 1.8, 6.0, 7.9, 6.8, 10.6, 7.0, 0, 8.3],
        [3.6, 13.0, 7.4, 10.1, 5.5, 7.2, 14.2, 10.7, 14.1, 6.0, 6.8, 6.4, 14.1, 10]
    ]

# Time Complexity: O(1) - constant time as it returns a predefined list
# Space Complexity: O(m) where m is the number of addresses
def load_address_data():
    """Load address data manually."""
    # Returns a predefined list of addresses
    return [
        "4001 south 700 east",
        "1060 dalton ave s",
        "1330 2100 s",
        "1488 4800 s",
        "177 w price ave",
        "195 w oakland ave",
        "2010 w 500 s",
        "2300 parkway blvd",
        "233 canyon rd",
        "2530 s 500 e",
        "2600 taylorsville blvd",
        "2835 main st",
        "300 state st",
        "3060 lester st",
        "3148 s 1100 w",
        "3365 s 900 w",
        "3575 w valley central station bus loop",
        "3595 main st",
        "380 w 2880 s",
        "410 s state st",
        "4300 s 1300 e",
        "4580 s 2300 e",
        "5025 state st",
        "5100 south 2700 west",
        "5383 s 900 east #104",
        "600 e 900 south",
        "6351 south 900 east"
    ]

# Time Complexity: O(n log n) due to the sorting operation
# Space Complexity: O(n) for storing all packages in different lists
def assign_packages_to_trucks(packages, num_trucks=3):
    """
    Assign packages to trucks based on various criteria.
    
    Why: Efficient package assignment is crucial for timely deliveries and meeting special requirements.
    What: This function distributes packages among available trucks considering deadlines and special notes.
    How:
    1. Initialize trucks and separate delayed packages from regular ones.
    2. Sort regular packages by deadline and special requirements.
    3. Assign high-priority packages to the first truck.
    4. Assign delayed and "truck 2 only" packages to the second truck.
    5. Distribute remaining packages among all trucks.
    """
    # Initialize the trucks
    trucks = [Truck(i+1) for i in range(num_trucks)]  # O(num_trucks) time
    all_packages = list(packages.all_packages())  # O(n) time, where n is the number of packages
    
    # Separate delayed packages
    delayed_packages = [p for p in all_packages if "Delayed" in p.notes]
    regular_packages = [p for p in all_packages if p not in delayed_packages]
    
    # Sort packages by deadline, with special requirements first
    regular_packages.sort(key=lambda p: (
        p.deadline == 'EOD',
        p.deadline,
        "Can only be on truck 2" not in p.notes,
        p.id not in [14, 15, 16, 19, 20]  # Prioritize grouped packages
    ))  # O(n log n) time due to sorting

    # Assign packages to trucks
    # The following loops are O(n) in total, as each package is processed once
    for package in regular_packages:
        if package.deadline != 'EOD' or package.id in [14, 15, 16, 19, 20]:
            if not trucks[0].is_full():
                trucks[0].load_package(package)
            else:
                break
    
    # Assign delayed and "truck 2 only" packages to the second truck
    for package in delayed_packages + [p for p in regular_packages if "Can only be on truck 2" in p.notes]:
        if not trucks[1].is_full():
            trucks[1].load_package(package)
    
    # Distribute remaining packages
    remaining_packages = [p for p in regular_packages if not any(p in t.packages for t in trucks)]
    for package in remaining_packages:
        assign_to_least_loaded_truck(package, trucks)
    
    return trucks


# Time Complexity: O(1) for EOD, O(1) for parsing time
# Space Complexity: O(1)
def time_to_minutes(time_str):
    if time_str == 'EOD':
        return 24 * 60  # End of day
    time_obj = datetime.strptime(time_str, "%I:%M %p")
    return time_obj.hour * 60 + time_obj.minute

# Time Complexity: O(t) where t is the number of trucks
# Space Complexity: O(1)
def assign_to_least_loaded_truck(package, trucks):
    least_loaded = min(trucks, key=lambda t: len(t.packages))
    if not least_loaded.is_full():
        least_loaded.load_package(package)
    else:
        print(f"Warning: Unable to assign package {package.id} to any truck.")

# Time Complexity: O(t) where t is the number of trucks
# Space Complexity: O(1)
def assign_to_truck(package, trucks):
    """Assign a package to the truck with the least packages."""
    least_loaded = min(trucks, key=lambda t: t.get_current_load())
    if not least_loaded.is_full():
        least_loaded.load_package(package)
    else:
        print(f"Warning: Unable to assign package {package.id} to any truck.")

# Time Complexity: O(m) where m is the number of addresses
# Space Complexity: O(1)
def find_closest_address(address, address_list):
    """Find the closest matching address in the list."""
    if address is None:
        return None
    address = address.lower()
    if address == "hub":
        return HUB_ADDRESS.lower()
    
    # More flexible string matching
    for addr in address_list:
        if all(word.lower() in addr.lower() for word in address.split()):
            return addr
    
    # If no exact match found, try partial matching
    for addr in address_list:
        if any(word.lower() in addr.lower() for word in address.split()):
            return addr
    
    print(f"Warning: No close match found for address: {address}")
    return address  # Return the original address if no match found

# Time Complexity: O(m) where m is the number of addresses
# Space Complexity: O(1)
def calculate_distance(addr1, addr2, distance_matrix, addresses):
    """Calculate distance between two addresses."""
    addr1 = find_closest_address(addr1, addresses)
    addr2 = find_closest_address(addr2, addresses)
    
    if addr1 is None or addr2 is None:
        print(f"Warning: Could not find close match for {addr1} or {addr2}")
        return 0
    
    try:
        index1 = addresses.index(addr1)
        index2 = addresses.index(addr2)
        return distance_matrix[index1][index2]
    except ValueError:
        print(f"Warning: Address not found in list: {addr1} or {addr2}")
        return 0
    except IndexError:
        print(f"Warning: Index out of range for addresses: {addr1} or {addr2}")
        return 0 

# Time Complexity: O(p^2 * m) where p is the number of packages and m is the number of addresses
# Space Complexity: O(p) for storing the route
def nearest_neighbor_algorithm(truck, distance_matrix, addresses):
    """
    Implement the Nearest Neighbor algorithm for package delivery.
     Why:
    This algorithm helps the truck deliver packages in the shortest possible route by visiting the nearest package first, 
      minimizing the total travel distance.

    What:
    It calculates the distance to each undelivered package, selects the nearest one, and repeats this process 
      until all packages are delivered. Finally, the truck returns to the hub.

    How:
    1. Copy the list of undelivered packages from the truck.
    2. Start from the hub address.
    3. For each iteration, find the nearest package based on the distance matrix.
    4. Calculate the distance, add it to the total, and remove the package from the undelivered list.
    5. After all deliveries, return to the hub and compute the total round-trip distance.
    """
    undelivered = truck.packages.copy()
    route = []
    current_location = HUB_ADDRESS.lower()
    total_distance = 0

    while undelivered:
        #Find nearest package
        nearest = min(undelivered, key=lambda p: calculate_distance(current_location, p.address, distance_matrix, addresses))
        distance = calculate_distance(current_location, nearest.address, distance_matrix, addresses)
        total_distance += distance
        route.append(nearest)
        current_location = nearest.address.lower()
        undelivered.remove(nearest)

    # Return to hub
    distance_to_hub = calculate_distance(current_location, HUB_ADDRESS.lower(), distance_matrix, addresses)
    total_distance += distance_to_hub

    return route, total_distance

# Time Complexity: O(p^2 * a) where p is the number of packages and a is the time to calculate distance
# This is because for each package (O(p)), we're finding the nearest among remaining packages (O(p * a))
# Space Complexity: O(p) for storing the route
def deliver_packages(truck, distance_matrix, addresses, current_time, packages):
    """
    Simulate the delivery of packages for a single truck.
    
    Why: This function is the core of the delivery simulation, handling the actual package delivery process.
    What: It determines the optimal route for package delivery and updates package statuses.
    How:
    1. Start the delivery process for the truck.
    2. While there are packages to deliver:
        a. Find available packages (considering delayed packages).
        b. Find the nearest package considering deadline and distance.
        c. Update package 9's address if it's time (special case).
        d. Calculate travel time and update current time.
        e. Deliver the package and update its status.
    3. Return to hub after all deliveries.
    """
    truck.start_delivery(current_time)
    route = []
    total_distance = 0
    DELIVERY_TIME = timedelta(minutes=2)
    UPDATE_TIME = datetime.strptime("10:20:00", "%H:%M:%S").time()
    DELAYED_ARRIVAL_TIME = datetime.strptime("09:05:00", "%H:%M:%S").time()

    while truck.packages:
        # Only consider packages that are available at the current time
        available_packages = [p for p in truck.packages 
                              if current_time >= p.available_time and
                              (not "Delayed" in p.notes or current_time.time() >= DELAYED_ARRIVAL_TIME)]
        if not available_packages:
            current_time += timedelta(minutes=1)
            continue
        
        
        # Update package 9's address if it's time
        if current_time.time() >= UPDATE_TIME:
            package_9 = next((p for p in truck.packages if p.id == 9), None)
            if package_9 and package_9.address != "410 S State St":
                package_9.address = "410 S State St"
                package_9.zip_code = "84111"
                print(f"Package #9 address updated at {current_time.strftime('%H:%M:%S')}")
         
        # Find nearest package
        nearest_package = min(available_packages, 
            key=lambda p: (time_to_minutes(p.deadline), 
                calculate_distance(truck.current_location, p.address, distance_matrix, addresses)))
        
        # Don't deliver package 9 before 10:20:00
        if nearest_package.id == 9 and current_time.time() < UPDATE_TIME:
            current_time += timedelta(minutes=1)
            continue

        # Deliver the package
        distance = calculate_distance(truck.current_location, nearest_package.address, distance_matrix, addresses)
        travel_time = timedelta(hours=distance / truck.speed)
        current_time += travel_time
        
        if truck.deliver_package(nearest_package, distance):
            current_time += DELIVERY_TIME
            total_distance += distance
            route.append(nearest_package)
            nearest_package.delivery_time = current_time
            nearest_package.delivery_truck = truck.truck_id 

            # Check if package was delivered on time
            deadline = datetime.strptime(nearest_package.deadline, "%I:%M %p") if nearest_package.deadline != "EOD" else datetime.strptime("17:00", "%H:%M")
            if current_time > deadline:
                print(f"Warning: Package {nearest_package.id} delivered late. Deadline: {nearest_package.deadline}, Delivered: {current_time.strftime('%I:%M %p')}")

    # Return to hub
    distance_to_hub = calculate_distance(truck.current_location, HUB_ADDRESS.lower(), distance_matrix, addresses)
    total_distance += distance_to_hub
    current_time += timedelta(hours=distance_to_hub / truck.speed)

    truck.end_delivery(current_time)
    truck.mileage = total_distance
    return total_distance, route, current_time



# Time Complexity: O(1)
# Space Complexity: O(1)
def get_package_status(package, time):
    if package is None:
        return "Package not found"
    
    update_time = datetime.strptime("10:20:00", "%H:%M:%S").time()
    delayed_arrival_time = datetime.strptime("09:05:00", "%H:%M:%S").time()

    # Special handling for delayed packages
    if "Delayed" in package.notes:
        if time.time() < delayed_arrival_time:
            return f'Delayed, will not arrive to depot until 09:05:00'
        elif time.time() >= delayed_arrival_time and (not package.delivery_time or time < package.delivery_time):
            return 'At the hub'

    # Special handling for Package 9
    if package.id == 9:
        if time.time() < update_time:
            return 'At the hub. Wrong address, will be updated at 10:20 AM.'
        elif time.time() >= update_time and (not package.delivery_time or time < package.delivery_time):
            return 'Address updated, en route'
    
    if package.delivery_time:
        if time < package.delivery_time:
            return 'En route'
        else:
            return f'Delivered at {package.delivery_time.strftime("%H:%M:%S")}'
    else:
        return 'At hub'

# Time Complexity: O(n * m), where n is the number of trucks and m is the total number of packages
# Space Complexity: O(m), where m is the total number of packages
def display_truck_package_status(trucks, packages, time):
    # Display the status of packages for each truck at a specific time.
    for i, truck in enumerate(trucks, 1):
        print(f"\nTruck {i} Packages:")
        
        # Display packages currently on the truck
        on_truck = [p for p in truck.packages if not p.delivery_time or p.delivery_time > time]
        for package in on_truck:
            status = get_package_status(package, time)
            print(f"Package {package.id}: {status}")
        
        # Display delivered packages for this truck
        delivered = [p for p in packages.all_packages() 
                     if p.delivery_time and p.delivery_time <= time 
                     and p not in truck.packages]
        if delivered:
            print("\nDelivered Packages:")
            for package in delivered:
                status = get_package_status(package, time)
                print(f"Package {package.id}: {status}")
        
        if not on_truck and not delivered:
            print("No packages assigned yet.")

    # Display packages not yet assigned to any truck
    unassigned = [p for p in packages.all_packages() 
                  if not any(p in t.packages for t in trucks) 
                  and (not p.delivery_time or p.delivery_time > time)]
    if unassigned:
        print("\nPackages not yet assigned to trucks:")
        for package in unassigned:
            status = get_package_status(package, time)
            print(f"Package {package.id}: {status}")

# Time Complexity: O(n), where n is the number of packages 
# Space Complexity: O(1), as it only uses a constant amount of extra space
def display_package_status(packages, time):
    """Display the status of all packages at a specific time."""
    print(f"\nPackage Status at {time.strftime('%H:%M:%S')}:")
    for i in range(1, 41):
        package = packages.lookup(i)
        if package:
            status = get_package_status(package, time)
            print(f"Package {i}: {status}")
        else:
            print(f"Package {i}: Not found")
            
# Time Complexity: O(1), as it performs constant time operations
# Space Complexity: O(1), as it returns a dictionary with a fixed number of fields           
def lookup_package_details(package_id, packages, current_time):
    """
    Look up detailed information for a specific package.
    """
    package = packages.lookup(package_id)
    if package is None:
        return "Package not found"
    
    status = get_package_status(package, current_time)
    
    # Special handling for Package 9
    update_time = datetime.strptime("10:20:00", "%H:%M:%S").time()
    if package.id == 9 and current_time.time() < update_time:
        address = "300 State St"
        zip_code = "84103"
    else:
        address = package.address
        zip_code = package.zip_code
    
    return {
        'delivery_address': address,
        'delivery_deadline': package.deadline,
        'delivery_city': package.city,
        'delivery_zip_code': zip_code,
        'package_weight': package.weight,
        'delivery_status': status,
        'delivery_time': package.delivery_time.strftime("%H:%M:%S") if package.delivery_time else "Not delivered yet"
    }


# Time Complexity: O(n), where n is the number of packages in the route
# Space Complexity: O(n), due to the string joining operation for the route
def print_truck_info(truck, route, distance):
    print(f"\nTruck {truck.truck_id}:")
    print(f"Route: {' -> '.join([p.address for p in route])}")
    print(f"Packages delivered: {len(route)}")
    print(f"Mileage: {distance:.2f} miles")
    for package in route:
        print(f"Delivered package {package.id} at {package.delivery_time}")

#Time Complexity: O(n*m),where n is the number of packages and m is the number of trucks
#Space Complexity: O(1) constant space
def display_all_package_status(packages, trucks, time):
    print(f"\nStatus of all packages at {time.strftime('%H:%M:%S')}:")
    print("ID | Address            | City            | State | ZIP   | Deadline | Weight | Status            | Truck")
    print("-" * 100)
    for i in range(1, 41):
        package = packages.lookup(i)
        if package:
            status = get_package_status(package, time)
            # Find which truck the package is on or was delivered by
            truck_num = "Not assigned"
            for t in trucks:
                if package in t.packages or (package.delivery_time and package.delivery_truck == t.truck_id):
                    truck_num = f"Truck {t.truck_id}"
                    break
            print(f"{package.id:2d} | {package.address[:20]:20s} | {package.city:15s} | {package.state:2s} | {package.zip_code:5s} | {package.deadline:8s} | {package.weight:6.1f} | {status:20s} | {truck_num}")
        else:
            print(f"{i:2d} | Not found")

# The main function runs the delivery simulation for each truck
# Time Complexity: O(t * p^2 * a) where t is the number of trucks, p is the average number of packages per truck,and a is the time to calculate distance
# Space Complexity: O(n) where n is the total number of packages, as we're storing all package data
def main():
    try:
        packages = load_package_data('WGUPS Package File.csv')
        distance_matrix = create_distance_matrix()
        addresses = load_address_data()

        # Add the HUB address if it's not already in the list
        hub_address = HUB_ADDRESS.lower()
        if hub_address not in addresses:
            addresses.append(hub_address)

        trucks = assign_packages_to_trucks(packages)
        total_mileage = 0
        current_time = START_TIME

        # Start trucks at different times
        truck_start_times = [
            START_TIME,
            START_TIME + timedelta(hours=1),  # Start second truck at 9:00 AM
            START_TIME + timedelta(hours=1, minutes=30)  # Start third truck at 9:30 AM
        ]

        for i, truck in enumerate(trucks, 1):
            current_time = truck_start_times[i-1]
            print(f"\nTruck {i} starting deliveries at {current_time.strftime('%H:%M:%S')}")
            try:
                distance, route, end_time = deliver_packages(truck, distance_matrix, addresses, current_time, packages)
                total_mileage += distance
                print_truck_info(truck, route, distance)
                print(f"Truck {i} finished deliveries at {end_time.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"An error occurred while delivering packages for Truck {i}: {str(e)}")

        print(f"\nTotal mileage for all trucks: {total_mileage:.2f} miles")
        latest_return_time = max(truck.return_time for truck in trucks if truck.return_time)
        print(f"All deliveries completed by: {latest_return_time.strftime('%H:%M:%S')}")

        while True:
            print("\n--- Main Menu ---")
            print("1. View details of all packages")
            print("2. Lookup package by ID")
            print("3. View total mileage of all trucks")
            print("4. View truck status")
            print("5. Lookup detailed package information for a specific time")
            print("6. Check status of all packages at a specific time")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                print("\nDetails of all packages:")
                for i in range(1, 41):
                    details = lookup_package_details(i, packages, latest_return_time)
                    if isinstance(details, dict):
                        print(f"\nPackage {i}:")
                        for key, value in details.items():
                            print(f"  {key.replace('_', ' ').title()}: {value}")
                    else:
                        print(f"\nPackage {i}: {details}")
            elif choice == '2':
                package_id = int(input("Enter package ID: "))
                details = lookup_package_details(package_id, packages, latest_return_time)
                if isinstance(details, dict):
                    print("\nPackage Details:")
                    for key, value in details.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print(details)
            elif choice == '3':
                print(f"Total mileage for all trucks: {total_mileage:.2f} miles")
            elif choice == '4':
                for i, truck in enumerate(trucks, 1):
                    print(f"Truck {i}: {len(truck.packages)} packages, {truck.mileage:.2f} miles traveled")
            elif choice == '5':
                package_id = int(input("Enter package ID: "))
                time_str = input("Enter time to check package status (HH:MM:SS): ")
                check_time = datetime.strptime(time_str, "%H:%M:%S")
                details = lookup_package_details(package_id, packages, check_time)
                if isinstance(details, dict):
                    print(f"\nPackage {package_id} Details at {check_time.strftime('%H:%M:%S')}:")
                    for key, value in details.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print(details)
            elif choice == '6':
                time_str = input("Enter time to check all package statuses (HH:MM:SS): ")
                check_time = datetime.strptime(time_str, "%H:%M:%S")
                display_all_package_status(packages, trucks, check_time)
            elif choice == '7':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
