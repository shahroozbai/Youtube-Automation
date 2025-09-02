# main.py
import datetime
from sheets_logger import log_to_sheets

def main():
    # Example: imagine your automation generated these
    topic = "Daily Motivation"
    video_title = "5 Habits of Successful People"
    youtube_url = "https://youtube.com/dummy-video-link"  # replace later with real upload URL

    # Log into Google Sheets
    try:
        log_to_sheets([
            datetime.datetime.utcnow().isoformat(),
            topic,
            video_title,
            youtube_url
        ])
        print("✅ Logged to Google Sheets successfully.")
    except Exception as e:
        print("❌ Failed to log to Google Sheets:", str(e))

if __name__ == "__main__":
    main()
