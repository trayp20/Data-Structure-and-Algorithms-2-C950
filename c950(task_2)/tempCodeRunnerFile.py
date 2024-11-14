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
        
        
        # Reset simulation_time to START_TIME for the main menu
        simulation_time = START_TIME


        while True:
            print("\n--- Main Menu ---")
            print("Current simulation time:", simulation_time.strftime("%H:%M:%S"))
            print("1. View status of all packages")
            print("2. Lookup package by ID")
            print("3. View total mileage of all trucks")
            print("4. View truck status")
            print("5. Simulate to a specific time")
            print("6. Lookup detailed package information by ID")
            print("7. Show status of all packages on each truck") 
            print("8. Check status of all packages at a specific time")
            print("11. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                display_package_status(packages, simulation_time)
            elif choice == '2':
                package_id = int(input("Enter package ID: "))
                package = packages.lookup(package_id)
                if package:
                    status = get_package_status(package, simulation_time)
                    print(f"Package {package_id} status: {status}")
                else:
                    print("Package not found")
            elif choice == '3':
                print(f"Total mileage for all trucks: {total_mileage:.2f} miles")
            elif choice == '4':
                for i, truck in enumerate(trucks, 1):
                    print(f"Truck {i}: {len(truck.packages)} packages, {truck.mileage:.2f} miles traveled")
            elif choice == '5':
                time_str = input("Enter time to simulate to (HH:MM:SS): ")
                new_time = datetime.strptime(time_str, "%H:%M:%S")
                if new_time < simulation_time:
                    print("Cannot simulate to a time earlier than the current simulation time.")
                else:
                    simulation_time = new_time
                    print(f"Simulation time updated to {simulation_time.strftime('%H:%M:%S')}")
            elif choice == '6':
                package_id = int(input("Enter package ID for detailed lookup: "))
                details = lookup_package_details(package_id, packages, simulation_time)
                if isinstance(details, dict):
                    print("\nPackage Details:")
                    for key, value in details.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print(details)
            elif choice == '7':
                display_truck_package_status(trucks, packages, simulation_time)
            elif choice == '8':
                time_str = input("Enter time to check package status (HH:MM:SS): ")
                check_time = datetime.strptime(time_str, "%H:%M:%S")
                display_all_package_status(packages, trucks, check_time)
            elif choice == '11':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")