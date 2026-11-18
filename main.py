from parser import parse_logs
from analyzer import analyze_traffic
from validator import get_invalid_ips
from security import flag_excessive_logins

def main():
    print("=" * 50)
    print("       CAMPUS WI-FI LOG ANALYSER       ")
    print(" [SDG 9: Infrastructure | SDG 4: Education]")
    print("=" * 50)
    
    # 1. Parse the raw text file
    print("\nReading wifi_logs.txt...")
    logs = parse_logs("wifi_logs.txt")
    
    if not logs:
        print("Process terminated: No data found.")
        return
        
    # 2. Pass the data through the three analysis modules
    student_totals, busy_hr, peak_volume = analyze_traffic(logs)
    bad_ips = get_invalid_ips(logs)
    security_alerts = flag_excessive_logins(logs)
    
    # 3. Format the final output for the lab report screenshot
    print("\n[1] NETWORK TRAFFIC ANALYSIS")
    print(f"    -> Busiest Hour: {busy_hr}:00 (Peak volume: {peak_volume} actions)")
    print(f"    -> Total Unique Students Connected: {len(student_totals)}")
    
    print("\n[2] SECURITY: RATE LIMITING (>5 logins/hr)")
    if security_alerts:
        for alert in security_alerts:
            print(f"    [!] FLAGGED: USN {alert['usn']} logged in {alert['count']} times during {alert['hour']}:00")
    else:
        print("    -> No rate-limit violations detected.")
        
    print("\n[3] NETWORK VALIDATION: INVALID IPs")
    if bad_ips:
        for ip in bad_ips:
            print(f"    [X] INVALID FORMAT: {ip}")
    else:
        print("    -> All logged IP addresses are structurally valid.")
        
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
