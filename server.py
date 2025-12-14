

import json
import socket
import threading
import sys
import time

CONFIG_File = "config.json"

def load_config(path):
    with open(path, 'r', encoding="utf-8") as f:
        return json.load(f)

def udp_server (port, name, stop_event):
    host = "0.0.0.0"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.settimeout(1.0)

        print(f"[UDP] {name} hört auf {host}:{port}")

        while not stop_event.is_set():
            try:
                data, addr = s.recvfrom(1024)
            except socket.timeout:
                    continue

            print(f"[UDP] Paket von {addr} aud {name}: {data!r}")
            s.sendto(b"OK_UDP: " + data, addr)

    print(f"[UDP] {name} sauber beendet")


def main():

    stop_event = threading.Event()
    threads = []

    config_path = CONFIG_File
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    config = load_config(config_path)
    tests = config.get("tests", [])

    if not tests:
        print("keine Tests in der Konfiguration definiert.")
        return

    for entry in tests:
        port = entry["port"]
        proto = entry["protocol"].lower()
        name = entry.get("name", f"Port {port}/{proto}")

        if proto == "tcp":
            #TODO tcp Logic
            print("tcp will be used here")
        elif proto == "udp":
            t = threading.Thread(
                target=udp_server,
                args=(port, name, stop_event)
                )
            t.start()
            threads.append(t)
        else:
            print(f"unbekanntes Protokoll in Config: {proto} (Port {port})")

    print("Server läuft. Strg + c zum Beenden.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Server wird jetzt beendet")
        stop_event.set()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
