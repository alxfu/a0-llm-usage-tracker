from helpers.extension import Extension
import time
import os
from datetime import datetime

class RequestsBanner(Extension):
    async def execute(self, banners: list = [], frontend_context: dict = {}, **kwargs):
        log_file = "/a0/usr/workdir/llm_requests.log"
        count = 0
        now = time.time()
        twenty_four_hours_ago = now - (24 * 3600)
        
        valid_lines = []
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        timestamp = float(line)
                        if timestamp >= twenty_four_hours_ago:
                            valid_lines.append(line + "\n")
                            count += 1
                    except ValueError:
                        try:
                            dt_str = line.split(" - ")[0]
                            dt = datetime.fromisoformat(dt_str)
                            if dt.timestamp() >= twenty_four_hours_ago:
                                valid_lines.append(line + "\n")
                                count += 1
                        except Exception:
                            pass
                            
                with open(log_file, "w") as f:
                    f.writelines(valid_lines)
            except Exception as e:
                print(f"Error reading requests log: {e}")

        banners.append({
            "id": "requests-per-day",
            "type": "info",
            "priority": 20,
            "title": "LLM Requests (24h)",
            "html": f"<div style='font-size: 24px; font-weight: bold; text-align: center; padding: 10px;'>{count}</div>",
            "dismissible": False,
            "source": "backend",
        })
