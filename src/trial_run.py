import csv

# Function to calculate time difference in minutes
def calculateDuration(departure, arrival):
    dep_hour, dep_min = departure.split(":")
    arr_hour, arr_min = arrival.split(":")
    dep_total = int(dep_hour) * 60 + int(dep_min)
    arr_total = int(arr_hour) * 60 + int(arr_min)
    if arr_total < dep_total:
        arr_total += 24 * 60
    return arr_total - dep_total

# Compares two time strings in "HH:MM" format
def isTimeAfter(time1, time2):
    h1, m1 = time1.split(":")
    h2, m2 = time2.split(":")
    h1, m1, h2, m2 = int(h1), int(m1), int(h2), int(m2)
    return h1 > h2 or (h1 == h2 and m1 >= m2)

# Loads flight data from the CSV file
def getData(filename):
    flights = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure the row is not empty
                    airline = row[0]
                    flight_number = row[1]
                    departure_time = row[2]
                    arrival_time = row[3]
                    price = float(row[4].replace('$', ''))
                    flights.append([airline, flight_number, departure_time, arrival_time, price])
    except FileNotFoundError:
        print(f"Invalid file name try again...")
    except ValueError as e:
        print(f"Error processing file: {e}")
    return flights

# Option 1: Find Specific Flight (case-sensitive airline name)
def findSpecificFlight(airline, flight_number, flights):
    while True:
        airline = input("Enter airline name: ").strip()
        airline_found = False
        for flight in flights:
            if flight[0] == airline:
                airline_found = True
                break
        if airline_found:
            break
        print("Invalid input -- try again")

    while True:
        flight_number = input("Enter flight number: ").strip()
        if flight_number.isdigit():
            break
        print("Invalid input -- try again")

    result = None
    for flight in flights:
        if flight[0] == airline and flight[1] == flight_number:
            result = flight
            break

    if result:
        print("\nThe flight that meets your criteria is:\n")
        print("AIRLINE".ljust(10), "FLT#".rjust(6), "DEPART".rjust(8), "ARRIVE".rjust(8), "PRICE".rjust(6))
        print(f"{result[0].ljust(10)} {result[1].rjust(6)} {result[2].rjust(8)} {result[3].rjust(8)} ${int(result[4]):>6}")
    else:
        print("Flight not found.")

# Option 2: Flights Shorter than a Specified Duration
def durationFilter(max_duration, flights):
    while True:
        try:
            max_duration = int(input("Enter maximum duration (in minutes): ").strip())
            break
        except ValueError:
            print("Entry must be a number")

    filtered_flights = []
    for flight in flights:
        duration = calculateDuration(flight[2], flight[3])
        if duration <= max_duration:
            filtered_flights.append(flight)

    if filtered_flights:
        print("\nThe flights that meet your criteria are:\n")
        print("AIRLINE".ljust(10), "FLT#".rjust(6), "DEPART".rjust(8), "ARRIVE".rjust(8), "PRICE".rjust(6))
        for flight in filtered_flights:
            print(f"{flight[0].ljust(10)} {flight[1].rjust(6)} {flight[2].rjust(8)} {flight[3].rjust(8)} ${int(flight[4]):>6}")
    else:
        print("No flights meet your criteria")

# Option 3: Cheapest Flight by a Given Airline
def findCheapestFlight(airline, flights):
    while True:
        airline = input("Enter airline name: ").strip()
        airline_found = False
        for flight in flights:
            if flight[0] == airline:  # Exact match for airline (case-sensitive)
                airline_found = True
                break
        if airline_found:
            break
        print("Invalid input -- try again")

    cheapest_flight = None
    for flight in flights:
        if flight[0] == airline:
            if cheapest_flight is None or flight[4] < cheapest_flight[4]:
                cheapest_flight = flight

    if cheapest_flight:
        print("\nThe flight that meets your criteria is:\n")
        print("AIRLINE".ljust(10), "FLT#".rjust(6), "DEPART".rjust(8), "ARRIVE".rjust(8), "PRICE".rjust(6))
        print(f"{cheapest_flight[0].ljust(10)} {cheapest_flight[1].rjust(6)} {cheapest_flight[2].rjust(8)} {cheapest_flight[3].rjust(8)} ${int(cheapest_flight[4]):>6}")
    else:
        print("No flights found for the specified airline")

# Option 4: Flights Departing After a Specified Time
def departureTimeFilter(time, flights):
    time = input("Enter earliest departure time: ").strip()  # Prompt only once
    while not (len(time) == 5 and time[2] == ":" and time[:2].isdigit() and time[3:].isdigit() and 
               0 <= int(time[:2]) < 24 and 0 <= int(time[3:]) < 60):
        time = input("Invalid time - Try again: ").strip()  # Same line for retry

    filtered_flights = []
    for flight in flights:
        if isTimeAfter(flight[2], time):
            filtered_flights.append(flight)

    if filtered_flights:
        print("\nThe flights that meet your criteria are:\n")
        print("AIRLINE".ljust(10), "FLT#".rjust(6), "DEPART".rjust(8), "ARRIVE".rjust(8), "PRICE".rjust(6))
        for flight in filtered_flights:
            print(f"{flight[0].ljust(10)} {flight[1].rjust(6)} {flight[2].rjust(8)} {flight[3].rjust(8)} ${int(flight[4]):>6}")
    else:
        print("No flights meet your criteria")

# Option 5: Average Price of All Flights
def averagePriceCalculator(flights):
    if not flights:
        print("No flights available to calculate the average price.")
        return
    total_price = 0
    for flight in flights:
        total_price += flight[4]
    average_price = total_price / len(flights)
    print(f"The average price is $ {average_price:.2f}")

# Option 6: Sort Flights by Departure Time and Write to a File
def sortByDeparture(flights):
    n = len(flights)
    for i in range(n):
        for j in range(0, n - i - 1):
            dep_time1 = flights[j][2].split(":")
            dep_time2 = flights[j + 1][2].split(":")
            h1, m1 = int(dep_time1[0]), int(dep_time1[1])
            h2, m2 = int(dep_time2[0]), int(dep_time2[1])
            total_minutes1 = h1 * 60 + m1
            total_minutes2 = h2 * 60 + m2
            if total_minutes1 > total_minutes2:
                flights[j], flights[j + 1] = flights[j + 1], flights[j]
    return flights

def writeSortedFlights(sorted_flights, filename="time-sorted-flights.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Airline", "Flight Number", "Departure Time", "Arrival Time", "Price"])
        for flight in sorted_flights:
            writer.writerow([flight[0], flight[1], flight[2], flight[3], f"${int(flight[4])}"])
    print(f"Sorted data has been written to file: {filename}")

# Main Function
def main():
    flights = []
    while not flights:
        filename = input("Please enter a file name: ")
        flights = getData(filename)
        if not flights:
            print("Invalid file name, try again ...")

    choice = 0
    while choice != 7:  # Loop until the user chooses to quit
        print("\nPlease choose one of the following options:")
        print("1 -- Find flight information by airline and flight number")
        print("2 -- Find flights shorter than a specified duration")
        print("3 -- Find the cheapest flight by a given airline")
        print("4 -- Find flight departing after a specified time")
        print("5 -- Find the average price of all flights")
        print("6 -- Write a file with flights sorted by departure time")
        print("7 -- Quit")

        try:
            choice = int(input("Choice ==> "))
        except ValueError:
            print("Entry must be a number")
            continue

        if choice < 1 or choice > 7:
            print("Entry must be between 1 and 7")
            continue

        if choice == 1:
            findSpecificFlight("", "", flights)
        elif choice == 2:
            durationFilter(0, flights)
        elif choice == 3:
            findCheapestFlight("", flights)
        elif choice == 4:
            departureTimeFilter("", flights)
        elif choice == 5:
            averagePriceCalculator(flights)
        elif choice == 6:
            sorted_flights = sortByDeparture(flights.copy())
            writeSortedFlights(sorted_flights)
        elif choice == 7:
            print("Thank you for flying with us")
            break
