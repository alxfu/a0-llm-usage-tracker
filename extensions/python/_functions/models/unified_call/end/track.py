from helpers.extension import Extension
import time
import json

class TrackRequest(Extension):
    async def execute(self, result, *args, **kwargs):
        # result is Tuple[str, str] -> (response_text, reasoning_text)
        response_text, reasoning_text = result
        
        # Extract model name from the ChatModel instance (args[0])
        model_instance = args[0] if len(args) > 0 else None
        model_name = getattr(model_instance, "model_name", "unknown")
        
        # Calculate input length
        input_chars = 0
        messages = kwargs.get("messages")
        if messages:
            for msg in messages:
                input_chars += len(str(getattr(msg, "content", "")))
        else:
            input_chars += len(str(kwargs.get("system_message", "")))
            input_chars += len(str(kwargs.get("user_message", "")))
        
        log_data = {
            "timestamp": time.time(),
            "model": model_name,
            "input_chars": input_chars,
            "output_chars": len(response_text) if response_text else 0,
            "reasoning_chars": len(reasoning_text) if reasoning_text else 0
        }
        
        log_file = "/a0/usr/workdir/llm_requests.log"
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception as e:
            print(f"Error logging request: {e}")
            
        return result
