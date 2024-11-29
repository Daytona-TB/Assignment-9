def write_most_popular_airport(filepath, output_filepath):
    # Open the CSV file and read its lines
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

    # Check if the file has at least a header and some data
    if len(lines) < 2:
        print("Error: The file is empty or does not have sufficient data.")
        return

    # Read the header line and split it, cleaning up extra spaces or quotes
    header = [h.strip().strip('"') for h in lines[0].strip().split(',')]

    # Get indices for necessary columns with error handling
    try:
        destination_airport_index = header.index("Destination_airport")
        fly_date_index = header.index("Fly_date")
        flights_index = header.index("Flights")
    except ValueError:
        print("Error: One or more required columns ('Destination_airport', 'Fly_date', 'Flights') are not found in the file.")
        return

    # Dictionary to hold flight counts per airport for each month
    monthly_airport_flights = {}

    # Iterate through each line in the file, starting from the second line (skip the header)
    for line in lines[1:]:
        parts = [p.strip().strip('"') for p in line.strip().split(',')]

        # Ensure the line has enough columns to avoid IndexError
        if len(parts) > max(destination_airport_index, fly_date_index, flights_index):
            try:
                destination_airport = parts[destination_airport_index]
                fly_date = parts[fly_date_index]
                flights = int(parts[flights_index])
            except (IndexError, ValueError):
                # Skip lines with missing or invalid data
                continue

            # Extract the month from the fly_date (assuming the format is YYYY-MM-DD)
            month = fly_date[:7]

            # Initialize the dictionary for this month if not already present
            if month not in monthly_airport_flights:
                monthly_airport_flights[month] = {}

            # Add the flight count to the destination airport for this month
            if destination_airport in monthly_airport_flights[month]:
                monthly_airport_flights[month][destination_airport] += flights
            else:
                monthly_airport_flights[month][destination_airport] = flights

    # Determine the most popular airport for each month and write to the output file
    try:
        with open(output_filepath, 'w') as output_file:
            output_file.write("Month,Most_Popular_Airport,Flight_Count\n")

            # Iterate through the monthly data to find the airport with the most flights
            for month, airports in monthly_airport_flights.items():
                most_popular_airport = None
                max_flights = 0

                # Find the airport with the maximum flights
                for airport, flight_count in airports.items():
                    if flight_count > max_flights:
                        most_popular_airport = airport
                        max_flights = flight_count

                # Write the result to the output file
                if most_popular_airport:
                    output_file.write(f"{month},{most_popular_airport},{max_flights}\n")
    except FileNotFoundError:
        print("Error: Unable to create or write to the output file.")
        return

    print(f"Most popular airports for each month have been written to {output_filepath}")

# Filepath to your CSV
filepath = "/Users/lucashandlon/Desktop/Information Infrastructure/Airports2.csv"
output_filepath = "/Users/lucashandlon/Desktop/Information Infrastructure/Most_Popular_Airports.csv"
write_most_popular_airport(filepath, output_filepath)
