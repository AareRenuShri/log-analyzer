import random
from datetime import datetime, timedelta

ERROR_MESSAGES = [
    "Failed to connect to database",
    "Timeout on request",
    "Authentication token expired",
    "Null pointer exception in payment module ",
    "Disk space critically low",
]

WARNING_MESSAGES = [
    "High memory usage",
    "Slow query detected",
    "Deprecated API endpoint called",
    "Retry limit approaching",
]

INFO_MESSAGES = [
    "User logged in",
    "User logged out",
    "User viewed dashboard",
    "New user registered",
    "Payment processed successfully",
]

def generate_log_line(current_time):
    """Randomly build one realistic log line."""
    level = random.choices(["ERROR", "WARNING", "INFO"], weights=[60, 25, 15], k=1)[0]
    
    if level == "ERROR":
        message = random.choice(ERROR_MESSAGES)
    elif level == "WARNING":
        message = random.choice(WARNING_MESSAGES)
    else:
        message = random.choice(INFO_MESSAGES)
        
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} {level} {message}"

def main():
    num_lines = 500
    start_time = datetime(2026, 8, 1, 8, 0, 0)
    lines = []
    current_time = start_time
    
    for _ in range(num_lines):
        lines.append(generate_log_line(current_time))
        current_time += timedelta(seconds=random.randint(1, 300))
        
    with open("sample.log", "w") as file:
        file.writelines("\n".join(lines)+"\n")
        
    print(f"Generated {num_lines} log lines in 'sample.log'.")
    
if __name__ == "__main__":
    main()