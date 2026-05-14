import time
import os
from datetime import datetime

class SessionTracker:
    def __init__(self):
        self.start_time        = time.time()
        self.good_posture_time = 0
        self.bad_posture_time  = 0
        self.last_check_time   = time.time()
        self.current_status    = None

    def update(self, status):
        """Call this every frame with current posture status"""
        now       = time.time()
        elapsed   = now - self.last_check_time

        if self.current_status == "Good Posture":
            self.good_posture_time += elapsed
        elif self.current_status == "Bad Posture! Sit Up!":
            self.bad_posture_time += elapsed

        self.current_status  = status
        self.last_check_time = now

    def get_stats(self):
        """Returns formatted stats for display"""
        total    = self.good_posture_time + self.bad_posture_time
        if total == 0:
            good_pct = 0
            bad_pct  = 0
        else:
            good_pct = (self.good_posture_time / total) * 100
            bad_pct  = (self.bad_posture_time  / total) * 100

        session_duration = time.time() - self.start_time

        return {
            "duration"  : self.format_time(session_duration),
            "good_pct"  : round(good_pct, 1),
            "bad_pct"   : round(bad_pct, 1),
            "good_secs" : round(self.good_posture_time),
            "bad_secs"  : round(self.bad_posture_time)
        }

    def format_time(self, seconds):
        """Converts seconds to MM:SS format"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def save_log(self):
        """Saves session summary to CSV for Power BI"""
        stats     = self.get_stats()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_file  = "logs/posture_sessions.csv"

        # Create logs folder if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # Check if file exists to write header only once
        file_exists = os.path.exists(csv_file)

        with open(csv_file, "a", newline="") as f:
            import csv
            writer = csv.writer(f)

            # Write header only on first time
            if not file_exists:
                writer.writerow([
                    "date",
                    "duration_mmss",
                    "good_posture_pct",
                    "bad_posture_pct",
                    "good_posture_secs",
                    "bad_posture_secs"
                ])

            # Write this session's data as a new row
            writer.writerow([
                timestamp,
                stats["duration"],
                stats["good_pct"],
                stats["bad_pct"],
                stats["good_secs"],
                stats["bad_secs"]
            ])

        print(f"Log saved to {csv_file}")
        return csv_file