import sys
import re
from collections import Counter
import matplotlib.pyplot as plt

Log_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s(ERROR|WARNING|INFO)")

def read_log_file(filename):
    """Open the file and return a list of its lines."""
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines

def analyze_lines(lines):
    """Go through every lines and collect all our stats into a dictionary."""
    error_count = 0
    warning_count = 0
    info_count = 0
    errors_by_date = {}
    error_messages = []
    skipped_lines = 0
    
    for line in lines:
        match = Log_pattern.match(line)
        if not match:
            skipped_lines += 1
            continue
        
        if "ERROR" in line:
            error_count +=1
            date = line[:10]
            errors_by_date[date] = errors_by_date.get(date, 0) + 1
            message = line.split("ERROR",1)[1].strip()
            error_messages.append(message)
        elif "WARNING" in line:
            warning_count +=1
        elif "INFO" in line:
            info_count +=1
    
    return{
        "error_count": error_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "errors_by_date": errors_by_date,
        "error_messages": error_messages,
        "skipped_lines": skipped_lines
    }
        
def print_summary(stats, total_lines):
    """Print all the results in a readable format."""
    print(f"Total lines in log file:{total_lines}")
    
    if stats["skipped_lines"] > 0:
        word = "line" if stats["skipped_lines"] == 1 else "lines"
        print(f"\nSkipped {stats['skipped_lines']} {word} due to format issues.")
        
    print("\nLog level breakdown:")
    print(f"ERROR: {stats['error_count']}")
    print(f"WARNING: {stats['warning_count']}")
    print(f"INFO: {stats['info_count']}")
    
    if stats["error_messages"]:
        message_counts = Counter(stats["error_messages"])
        most_common_message, count = message_counts.most_common(1)[0]
        print(f"\nMost common error: \"{most_common_message}\" occurred {count} times.")
        
    print("\nErrors per day:")
    for date, count in sorted(stats["errors_by_date"].items()):
        print(f"{date}: {count} errors")
        
def save_chart(errors_by_date, output_file = "errors_chart.png"):
    """Create and save a bar chart of errors per day."""
    dates = sorted(errors_by_date.keys())
    counts = [errors_by_date[date] for date in dates]
    plt.bar(dates, counts, color = "#F28B82")
    plt.xlabel("Date")
    plt.ylabel("Number of Errors")
    plt.title("Errors per Day")
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"\nChart saved as {output_file}")
    
def save_pie_chart(error_messages, output_file = "error_reason_pie.png"):
    """Create and save a pie chart showing the breakdown of error reasons."""
    if not error_messages:
        return
    
    message_counts = Counter(error_messages)
    labels = list(message_counts.keys())
    sizes = list(message_counts.values())
    
    plt.figure()
    pastel_colors = ["#F28B82", "#FDCFE8", "#AECBFA", "#CCFF90", "#FFF475", "#D7AEFB"]
    wedges, texts, autotexts = plt.pie(sizes, autopct="%1.1f%%", startangle=90, colors=pastel_colors[:len(labels)])
    plt.axis('equal') 
    plt.title("Error Reasons Distribution")
    plt.legend(wedges, labels, title="Error Reasons", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"\nPie chart saved as {output_file}")
    
def main():
    if len(sys.argv) < 2:
        print("Please provide a log file. Example: python analyzer.py sample.log")
        sys.exit(1)

    filename = sys.argv[1]
    lines = read_log_file(filename)
    stats = analyze_lines(lines)
    print_summary(stats, len(lines))
    save_chart(stats["errors_by_date"])
    save_pie_chart(stats["error_messages"])

if __name__ == "__main__":
    main()