import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_log_with_ai(log_line):
    """Sends a single log line to the AI model for analysis."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Tier 3 SOC Analyst. Analyze this log entry. Output format: SEVERITY (Safe/Suspicious/Malicious) - Brief Explanation."},
                {"role": "user", "content": log_line}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {e}"

if __name__ == "__main__":
    log_file = "server.log"
    
    print(f"👀 Monitoring {log_file} for new threats... (Press Ctrl+C to stop)")
    
    # Open the file and jump to the end
    with open(log_file, "r") as f:
        # Move file pointer to the end of the file (0 bytes from the end)
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)  # Sleep briefly if no new data
                continue
            
            # If we found a new line, process it
            if line.strip():
                print(f"\n🔎 New Log Detected: {line.strip()}")
                analysis = analyze_log_with_ai(line)
                print(f"🤖 AI Verdict: {analysis}")
                print("-" * 50)
