import json
import os

CONFIG_PATH = "config.json"

def save_config(def_path, user_path):
    config = {
        "limits_definition": def_path,
        "limits_user": user_path
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None, None
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        return config.get("limits_definition"), config.get("limits_user")
