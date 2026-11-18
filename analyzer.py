def analyze_traffic(parsed_data):
    """
    Calculates total logins per student and identifies the busiest overall hour.
    Input: List of dictionaries (from parser.py)
    Output: Tuple containing (student_counts_dict, busiest_hour_string, max_traffic_int)
    """
    student_counts = {}
    hour_counts = {}
    
    # 1. Iterate through the parsed data to build our totals
    for entry in parsed_data:
        usn = entry["usn"]
        hour = entry["hour"]
        
        # Tally logins per student
        if usn in student_counts:
            student_counts[usn] += 1
        else:
            student_counts[usn] = 1
            
        # Tally total network activity per hour
        if hour in hour_counts:
            hour_counts[hour] += 1
        else:
            hour_counts[hour] = 1
            
    # 2. Find the busiest hour using standard foundational logic
    busiest_hour = ""
    max_traffic = 0
    
    for current_hour, count in hour_counts.items():
        if count > max_traffic:
            max_traffic = count
            busiest_hour = current_hour
            
    return student_counts, busiest_hour, max_traffic

# --- TEST THE ANALYZER ---
if __name__ == "__main__":
    # Import the function from your first file
    from parser import parse_logs 
    
    # Run the parser to get the data
    logs = parse_logs()
    
    # Pass the data into your new analyzer
    student_totals, busy_hr, peak_volume = analyze_traffic(logs)
    
    print(f"Busiest Hour: {busy_hr}:00 with {peak_volume} total network actions.\n")
    
    print("Login counts per student:")
    for student, count in student_totals.items():
        print(f"{student}: {count} logins")
