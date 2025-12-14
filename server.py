

import json
import socket
import threading
import sys

CONFIG_File = "server_config.json"

def load_config:(path):
    with open(path, 'r', encodings="utf-8") as f:
        return json.load(f)


def main():
    config_Path = CONFIG_File
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    config = load_config(config_path)
    listeners = config.get("listen", [])

    if not listeners:
        print("keine Listener in der Konfiguration definiert.")
        return

    for entry in listeners:
        port = entry["port"]
        proto = entry["protocol"].lower()
        name = entry.get("name", f"Port {port}/{proto}")

        if proto == "tcp":
            #TODO tcp Logic
            print("tcp will be used here")
        if proto == "udp":
            #TODO udp Logic
            print("udp Logic will be used here")
        else
            print("unbekanntes Protokoll in Config: {proto} (Port {port})")

    print("Server läuft. Strg + c zum Beenden.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n Server wird jetzt beendet")


if __name__ == "__main__":
    main()
