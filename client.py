
import json
import socket
import sys
import time

CONFIG_FILE = "config.json"

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config_path = CONFIG_FILE
    if len(sys.argv) > 1:              # these 2 lines can be deleted. Is for custom config path only.
        config_path = sys.argv[1]      # maybe it is used to specify an IP Address later, just for faster usage. The idea is that the config is mostly the same for every customer. The IP isnt.

    config = load_config(config_path)
    host = config["target_host"]
    timeout = float(config.get("timeout_sec", 2.0))
    tests = config.get("tests", [])

    if not tests:
        print("No tests in config defined.")
        return

    print(f"Start Connectiontests zu {host} (Timeout: {timeout}s)")
    print("-" * 60)

    results = []

    for t in tests:
        port = t["port"]
        proto = t["protocol"].lower()
        name = t.get("name", f"Port {port}/{proto}")

        print(port)
        print(proto)
        print(name)
        print("-" * 60)



if __name__ == "__main__":
    main()
