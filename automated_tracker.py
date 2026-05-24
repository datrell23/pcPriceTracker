"""
Automated Price Tracker
Runs the price scraper on a schedule at set intervals/ 
"""
import schedule
import time 
from main import main as run_scrapper


#Configs
CHECK_INTERVAL_HOURS = 6 #how often to check prices

def job():
    #Run price scrapper
    print("\n"+"="*50)
    print(f"Automated check started at {time.strftime('%Y-%m-%d %H:$M:%S')}")
    print("="*50)
    
    try:
        run_scrapper()
    except Exception as e:
        print(f"Error during scrapping: {e}")
        
    print("="*50)
    print(f"Check complete. Next check in {CHECK_INTERVAL_HOURS} hours")
    print("="*50 + "\n")
    
schedule.every(CHECK_INTERVAL_HOURS).hours.do(job)

print("Price Tracker Automation Started!")
print(f"Checking prices every {CHECK_INTERVAL_HOURS} hours")
print("Press Ctrl+C to stop\n")

job()

while True:
    schedule.run_pending()
    time.sleep(60)