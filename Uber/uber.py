import json

map = {"kolkata":10, "delhi": 20, "bangalore": 30, "mumbai": 40, "darjeeling": 50, "pune": 60}
map_keys = list(map.keys())
map_values = list(map.values())
vehicles = {"bike": 0.75, "auto": 1, "cab":1.25, }
vehicle_keys = list(vehicles.keys())
class Profiles:
        def __init__(self, name, age, rides_booked, money_spent, stars):
            self.name = name
            self.age = age
            self.rides_booked = rides_booked
            self.money_spent = money_spent
            self.stars = stars       

def load_data():
    try:
        with open('uber.txt', 'r') as file:
            test = json.load(file)
            return test
    except FileNotFoundError:
        return[]
    
def save_data_helper(rides):
    with open('uber.txt', 'w') as file:
        json.dump(rides, file)

def load_data_p():
    try:
        with open('profile.txt', 'r') as file:
            test = json.load(file)
            return test
    except FileNotFoundError:
        return[]

def save_data_helper_p(profiles):
    with open('profile.txt', 'w') as file:
        json.dump(profiles, file)


def open_map():
    print(map)

def book_ride(map, rides):
    while True:
        current_location = input("Enter your current location: ").strip().lower()
        if current_location not in map:
            print("Invalid Location")
        else:
            break

    while True:
        destination = input("Enter your destination: ").strip().lower()
        if destination not in map:
            print("Invalid Destination")
        else:
            break

    distance = abs(map[destination] - map[current_location])
    while True:
        choose_vehicle = input("Choose your vehicle: ").strip().lower()
        if choose_vehicle not in vehicle_keys:
            print("Invalid Vehicle")
        else:
            break

    base_fare = distance * 10
    final_fare = base_fare * vehicles[choose_vehicle]

    print("Your", choose_vehicle, "ride from", current_location, "to", destination, "of", distance, "kms, will cost you", final_fare, "rupees")
    confirmation = input("Please confirm your ride(yes/no): ")
    confirmation_lower = confirmation.lower()

    if confirmation_lower == "yes":
        print("Your ride to", destination, "has been booked")
        rides.append({'current_location': current_location, 'destination': destination, 'distance': distance, 'vehicle': choose_vehicle, 'fare': final_fare})
        save_data_helper(rides)
    elif confirmation_lower == "no":
        return main()
    else:
        return main()

def cancel_ride(rides):
    ride_history(rides)
    index = int(input("Enter the video number to be cancelled: "))

    if 1<= index <= len(rides):
        ride = rides[index-1]
        del rides[index-1]
        print(f"{index}. {ride['current_location']} to {ride['destination']}, distance covered {ride['distance']}kms, for rupees {ride['fare']}, in a {ride['vehicle']} has been cancelled")
        save_data_helper(rides)
    else:
        print("Invalid ride index selected")

def ride_history(rides):
    print("\n")
    print("*" * 100)
    for index, ride in enumerate(rides, start=1):
        print(f"{index}. {ride['current_location']} to {ride['destination']}, distance covered {ride['distance']}kms, for rupees {ride['fare']}, in a {ride['vehicle']} ")
    print("*" * 100)

def create_profile(profiles, rides):
 
 name = input("What is your name:  ")
 age = input("How old are you:  ")
 rides_booked = len(rides)
 money_spent = sum(ride['fare'] for ride in rides)
 stars = input("How many stars do you have:  ")
 profile = Profiles(name, age, rides_booked, money_spent, stars)
 profile = name
    
 profiles.append({'Name': name, 'Age': age, 'Rides booked': rides_booked, 'Money Spent': money_spent, 'Stars': stars})
 save_data_helper_p(profiles)

 print (f"{profile}'s profile has been created")

def list_profile(profiles):
    print("\n")
    print("*" * 100)
    for index, profile in enumerate(profiles, start=1):
        print(f"{index}. Name:{profile['Name']}, Age:{profile['Age']}, Rides Booked: {profile['Rides booked']}, Money Spent: {profile['Money Spent']}, Ratings:{profile['Stars']}stars ")
    print("*" * 100)

def edit_profile(profiles):
    list_profile(profiles)
    index = int(input("Enter the profile number you want to edit: "))
    if 1 <= index <= len(profiles):
        profile = profiles[index-1]
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        stars = input("Enter your stars: ")
        profiles[index-1] = {'Name': name, 'Age': age, 'Rides booked': profile.get('Rides booked', 0),
            'Money Spent': profile.get('Money Spent', 0),'Stars' : stars}
        save_data_helper_p(profiles)
        print(f"{profiles[index-1]['Name']}'s profile has been updated")
    else:
        print("Invalid Index no.")

def delete_profile(profiles):
    list_profile(profiles)
    index = int(input("Enter the profile number you want to delete: "))
    if 1 <= index <= len(profiles):
        del profiles[index-1]
        print(f"{profiles[index-1]}'s profile has been deleted successfully.")
    else:
        print("Invalid Index no.")

def show_profile(profiles):
    list_profile(profiles)
    index = int(input("Which profile do you want to view: "))
    if 1 <= index <= len(profiles):
        profile = profiles[index-1]
        print("*" * 100)
        print(f"{profile.get('Name')}'s profile")
        print(f"\nName: {profile.get('Name')}")
        print(f"Age: {profile.get('Age')}")
        print(f"Rides Booked: {profile.get('Rides booked')}")
        print(f"Money Spent: {profile.get('Money Spent')}")
        print(f"Stars: {profile.get('Stars')}")
        print("*" * 100)
    



def main():
    rides = load_data()
    profiles = load_data_p()
    while True:
        print("\n Weclome to Uber")
        print("1. Open Map")
        print("2. Book a ride")
        print("3. Cancel a ride")
        print("4. History of rides")
        print("5. Create your profile")
        print("6. List all profiles")
        print("7. Edit profile")
        print("8. Delete Profile")
        print("9. Show Profile")
        choice = int(input("Type your choice: "))

        if choice == 1:
            open_map()

        elif choice == 2:
            book_ride(map,rides)

        elif choice == 3:
            cancel_ride(rides)

        elif choice == 4:
            ride_history(rides)

        elif choice == 5:
            create_profile(profiles, rides)

        elif choice == 6:
            list_profile(profiles)
        
        elif choice == 7:
            edit_profile(profiles)

        elif choice == 8:
            delete_profile(profiles)

        elif choice == 9:
            show_profile(profiles)
        
        else:
            print("Invalid Input")


if __name__ == "__main__":
    main()
