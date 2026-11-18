def flag_excessive_logins(parsed_data):
    """
    Identifies students who logged in more than 5 times in a single hour.
    Input: List of dictionaries
    Output: List of dictionaries containing the flagged USN, the hour, and the count
    """
    # Dictionary to track logins. Key will be a tuple: (USN, Hour)
    login_tracker = {}
    flagged_users = []
    
    # 1. Tally the logins per hour for each student
    for entry in parsed_data:
        # We only care about LOGIN actions, not LOGOUTs
        if entry["action"] == "LOGIN":
            usn = entry["usn"]
            hour = entry["hour"]
            
            # Create a composite key to track this specific student at this specific hour
            tracker_key = (usn, hour)
            
            if tracker_key in login_tracker:
                login_tracker[tracker_key] += 1
            else:
                login_tracker[tracker_key] = 1
                
    # 2. Check the final totals to see who broke the rule
    for (usn, hour), count in login_tracker.items():
        if count > 5:
            flagged_users.append({
                "usn": usn, 
                "hour": hour, 
                "count": count
            })
            
    return flagged_users

# --- TEST THE SECURITY MONITOR ---
if __name__ == "__main__":
    from parser import parse_logs
    
    logs = parse_logs()
    security_alerts = flag_excessive_logins(logs)
    
    print(f"Security Alert: Found {len(security_alerts)} rate-limit violations.")
    for alert in security_alerts:
        print(f"- USN {alert['usn']} logged in {alert['count']} times during the {alert['hour']}:00 hour block.")
