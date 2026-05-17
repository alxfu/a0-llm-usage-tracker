from helpers.extension import Extension
import time

class TrackRequest(Extension):
    async def execute(self, result, *args, **kwargs):
        log_file = "/a0/usr/workdir/llm_requests.log"
        try:
            with open(log_file, "a") as f:
                f.write(f"{time.time()}\n")
        except Exception as e:
            print(f"Error logging request: {e}")
        return result
