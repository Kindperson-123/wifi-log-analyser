import re

def parse_logs(filename="wifi_logs.txt"):
    """
    Reads the log file line by line and extracts data using regex.
    Returns a list of dictionaries containing hour, usn, ip, and action.
    """
    parsed_data = []
    
    # REGEX BREAKDOWN:
    # (\d{2})           -> Group 1: Captures exactly 2 digits (the Hour).
    # \s+\d{2}\s+\d{2}  -> Skips over the minutes and seconds (no parentheses, so not captured).
    # \s+\|\s+USN\s+    -> Skips the spaces, the pipe '|', and the word 'USN '.
    # ([A-Z0-9]+)       -> Group 2: Captures the USN (letters and numbers).
    # \s+\|\s+          -> Skips the spaces and pipe.
    # ([a-zA-Z0-9.]+)   -> Group 3: Captures the IP. Notice we include letters so it catches your fake 'ABCD' IP for the validator to find later!
    # \s+\|\s+          -> Skips the spaces and pipe.
    # (LOGIN|LOGOUT)    -> Group 4: Captures the action (strictly looking for LOGIN or LOGOUT).
    
    pattern = re.compile(r" (\d{2})\s+\d{2}\s+\d{2}\s+\|\s+USN\s+([A-Z0-9]+)\s+\|\s+([a-zA-Z0-9.]+)\s+\|\s+(LOGIN|LOGOUT)")
    
    try:
        # Open in 'r' (read) mode
        with open(filename, 'r') as file:
            for line in file:
                match = pattern.search(line)
                
                if match:
                    # If the regex finds a match, pull out the 4 groups
                    log_entry = {
                        "hour": match.group(1),
                        "usn": match.group(2),
                        "ip": match.group(3),
                        "action": match.group(4)
                    }
                    parsed_data.append(log_entry)
                    
    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        
    return parsed_data

# --- TEST THE PARSER ---
if __name__ == "__main__":
    logs = parse_logs()
    
    print(f"Successfully parsed {len(logs)} lines.\n")
    
    # Print the first 3 parsed dictionaries just to prove it works
    print("Sample of extracted data:")
    for i in range(3):
        print(logs[i])
