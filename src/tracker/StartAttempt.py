import os
import json
import time

def ensure_timestamp_json(path="runtime/created.json"):
    if not os.path.exists(path):
        created_time = time.time()
        data = {
            "created": created_time,
            "created_human": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Created new file at {path} with timestamp.")
    else:
        print(f"File already exists at {path}.")


def read_timestamp_json(path="runtime/created.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            # print(f"File created at UNIX time: {data['created']}")
            # print(f"Human-readable time: {data['created_human']}")
            return data
    except FileNotFoundError:
        print(f"No file found at {path}.")
        return None
    except json.JSONDecodeError:
        print(f"File at {path} is not valid JSON.")
        return None

def json_exists(path="runtime/created.json"):
    return os.path.exists(path)