def get_invalid_ips(parsed_data):
    """
    Scans the parsed logs for structurally invalid IPv4 addresses.
    Input: List of dictionaries
    Output: List of unique invalid IP strings
    """
    # Using a Set ensures we don't list the same bad IP 50 times if it spams the network
    invalid_ips = set()
    
    for entry in parsed_data:
        ip = entry["ip"]
        
        # Break the IP into its chunks (e.g., "192.168.1.15" becomes ["192", "168", "1", "15"])
        octets = ip.split('.')
        
        # Rule 1: An IPv4 address MUST have exactly 4 sections
        if len(octets) != 4:
            invalid_ips.add(ip)
            continue
            
        # Rule 2: Check each individual section
        for octet in octets:
            # Check if it contains letters (catches your injected 'ABCD' edge case)
            if not octet.isdigit():
                invalid_ips.add(ip)
                break
                
            # Check if the number violates standard IP math (catches your '300' and '999')
            if int(octet) < 0 or int(octet) > 255:
                invalid_ips.add(ip)
                break
                
    # Convert the Set back to a standard List before returning it
    return list(invalid_ips)

# --- TEST THE VALIDATOR ---
if __name__ == "__main__":
    from parser import parse_logs
    
    logs = parse_logs()
    bad_ips = get_invalid_ips(logs)
    
    print(f"Found {len(bad_ips)} invalid IP addresses in the logs:")
    for bad_ip in bad_ips:
        print(f"- {bad_ip}")
