def write_most_popular_airport(filepath, output_filepath):
    # Open the CSV file and read its lines
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
        print(f"Total lines read (including header): {len(lines)}")
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

    # Check if the file has at least a header and some data
    if len(lines) < 2:
        print("Error: The file is empty or does not have sufficient data.")
        return

    # Read the header line and split it, cleaning up extra spaces or quotes
    header = custom_split(lines[0].strip())
    header = [h.strip().strip('"') for h in header]
    print(f"Header columns: {header}")

    # Get indices for necessary columns with error handling
    try:
        destination_airport_index = header.index("Destination_airport")
        fly_date_index = header.index("Fly_date")
        flights_index = header.index("Flights")
        print(f"Indices found - Destination Airport: {destination_airport_index}, Fly Date: {fly_date_index}, Flights: {flights_index}")
    except ValueError as e:
        print(f"Error: Required columns are not found in the file. Details: {e}")
        return

    # Dictionary to hold flight counts per airport for each month
    monthly_airport_flights = {}

    # Iterate through each line in the file, starting from the second line (skip the header)
    for line_number, line in enumerate(lines[1:], start=2):  # Start line count at 2 to account for the header
        parts = custom_split(line.strip())
        parts = [p.strip().strip('"') for p in parts]

        # Debug: print parsed parts
        print(f"Parsed parts for line {line_number}: {parts}")

        # Ensure there are enough columns
        if len(parts) <= max(destination_airport_index, fly_date_index, flights_index):
            print(f"Skipping line {line_number}: not enough columns.")
            continue

        try:
            destination_airport = parts[destination_airport_index]
            fly_date = parts[fly_date_index]
            flights = int(parts[flights_index]) if parts[flights_index].isdigit() else 0
        except (IndexError, ValueError) as e:
            # Log and continue in case of parsing issues
            print(f"Skipping line {line_number} due to parsing error: {e}")
            print(f"Problematic line content: {line}")
            continue

        # Extract the month from the fly_date (assuming the format is YYYY-MM-DD)
        if len(fly_date) >= 7 and '-' in fly_date:
            month = fly_date[:7]  # Extract the "YYYY-MM" part
        else:
            print(f"Skipping line {line_number}: invalid date format '{fly_date}'")
            print(f"Problematic line content: {line}")
            continue

        # Debug: print the current processing line details
        print(f"Processing line {line_number}: Month: {month}, Airport: {destination_airport}, Flights: {flights}")

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
                if not airports:
                    print(f"No data for month {month}, skipping...")
                    continue

                most_popular_airport = max(airports, key=airports.get)
                max_flights = airports[most_popular_airport]

                # Write the result to the output file
                output_file.write(f"{month},{most_popular_airport},{max_flights}\n")
                print(f"Written to file: Month: {month}, Most Popular Airport: {most_popular_airport}, Flight Count: {max_flights}")
    except FileNotFoundError:
        print("Error: Unable to create or write to the output file.")
        return

    print(f"Most popular airports for each month have been written to {output_filepath}")


def custom_split(line):
    """
    Custom function to split CSV lines, accounting for quoted fields.
    """
    parts = []
    current = ""
    inside_quotes = False

    for char in line:
        if char == '"' and not inside_quotes:
            inside_quotes = True
            current += char
        elif char == '"' and inside_quotes:
            inside_quotes = False
            current += char
        elif char == ',' and not inside_quotes:
            parts.append(current)
            current = ""
        else:
            current += char

    # Append the last part
    if current:
        parts.append(current)

    return parts

# Filepath to your CSV
filepath = "/Users/lucashandlon/Desktop/Information Infrastructure/Airports2.csv"
output_filepath = "/Users/lucashandlon/Desktop/Information Infrastructure/Most_Popular_Airports.csv"
write_most_popular_airport(filepath, output_filepath)
