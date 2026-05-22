from helpers.extension import Extension
import time
import os
import json
from datetime import datetime

class RequestsBanner(Extension):
    async def execute(self, banners: list = [], frontend_context: dict = {}, **kwargs):
        log_file = "/a0/usr/workdir/llm_requests.log"
        now = time.time()
        twenty_four_hours_ago = now - (24 * 3600)
        
        count = 0
        models = {}
        total_in_chars = 0
        total_out_chars = 0
        total_reasoning_chars = 0
        
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
                        # Try parsing as JSON (new format)
                        data = json.loads(line)
                        timestamp = data.get("timestamp", 0)
                        if timestamp >= twenty_four_hours_ago:
                            valid_lines.append(line + "\n")
                            count += 1
                            
                            model = data.get("model", "unknown")
                            models[model] = models.get(model, 0) + 1
                            
                            total_in_chars += data.get("input_chars", 0)
                            total_out_chars += data.get("output_chars", 0)
                            total_reasoning_chars += data.get("reasoning_chars", 0)
                    except json.JSONDecodeError:
                        # Fallback for old float format
                        try:
                            timestamp = float(line)
                            if timestamp >= twenty_four_hours_ago:
                                valid_lines.append(line + "\n")
                                count += 1
                                models["unknown"] = models.get("unknown", 0) + 1
                        except ValueError:
                            pass
                            
                with open(log_file, "w") as f:
                    f.writelines(valid_lines)
            except Exception as e:
                print(f"Error reading requests log: {e}")

        # Format model breakdown
        model_html = "".join([f"<div style='font-size: 12px; opacity: 0.8;'>{m}: <b>{c}</b></div>" for m, c in models.items()])
        if not model_html:
            model_html = "<div style='font-size: 12px; opacity: 0.5;'>No data</div>"
            
        # Format volume
        in_k = total_in_chars / 1000
        out_k = total_out_chars / 1000
        reason_k = total_reasoning_chars / 1000
        
        banners.append({
            "id": "requests-per-day",
            "type": "info",
            "priority": 20,
            "title": "LLM Usage (24h)",
            "html": f"""
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 5px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 11px; text-transform: uppercase; opacity: 0.6;'>Requests</div>
                    <div style='font-size: 20px; font-weight: bold;'>{count}</div>
                </div>
                <div style='border-left: 1px solid rgba(255,255,255,0.1); padding-left: 15px;'>
                    <div style='font-size: 11px; text-transform: uppercase; opacity: 0.6; margin-bottom: 4px;'>Models</div>
                    {model_html}
                </div>
                <div style='border-left: 1px solid rgba(255,255,255,0.1); padding-left: 15px;'>
                    <div style='font-size: 11px; text-transform: uppercase; opacity: 0.6; margin-bottom: 4px;'>Volume (Chars)</div>
                    <div style='font-size: 12px; opacity: 0.8;'>In: <b>{in_k:.1f}k</b></div>
                    <div style='font-size: 12px; opacity: 0.8;'>Out: <b>{out_k:.1f}k</b></div>
                    <div style='font-size: 12px; opacity: 0.8;'>Think: <b>{reason_k:.1f}k</b></div>
                </div>
            </div>
            """,
            "dismissible": False,
            "source": "backend",
        })
