class ParkingLot:
    def __init__(self):
        self.parking_spaces = {} 
        for level in ['A', 'B']:
            for spot_number in range(1, 21):
                self.parking_spaces[level + str(spot_number)] = None

    def assign_parking_space(self, vehicle_number):
        for spot, vehicle in self.parking_spaces.items():
            if vehicle is None:
                self.parking_spaces[spot] = vehicle_number
                return {"level": spot[0], "spot": int(spot[1:])}
        return None  

    def retrieve_parking_spot(self, vehicle_number):
        for spot, vehicle in self.parking_spaces.items():
            if vehicle == vehicle_number:
                return {"level": spot[0], "spot": int(spot[1:])}
        return None  

def main():
    parking_lot = ParkingLot()

    while True:
        print("Choose an operation:")
        print("1. Assign a parking space to a new vehicle")
        print("2. Retrieve parking spot number for a vehicle")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_number = input("Enter the vehicle number: ")
            result = parking_lot.assign_parking_space(vehicle_number)
            if result:
                print(f"Assigned parking space: {result}")
            else:
                print("Parking lot is full.")
        elif choice == "2":
            vehicle_number = input("Enter the vehicle number: ")
            result = parking_lot.retrieve_parking_spot(vehicle_number)
            if result:
                print(f"Retrieved parking space for vehicle {vehicle_number} : {result}")
            else:
                print("Vehicle not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
