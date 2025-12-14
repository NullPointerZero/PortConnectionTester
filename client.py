
import json
import socket
import sys
import time

CONFIG_FILE = "config.json"

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_udp(host, port, timeout):
    start = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRA) as s:
        s.settimout(timeout)
        try:
            s.sendto(b"PING_UDP", (host, port))
            data, addr = s.recvfrom(1024)
            latency_ms = (time.time() - start)*1000
            return True, latency_ms, data.decode(errors="replace")
        except Exception as e:
            return False, None, str(e)


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

        if (proto == "udp"):
            # TODO UDP Testfunction
            print("udp will be testet here")
        if (proto == "tcp"):
            ## TODO TCP Testfunction
            print("tcp will be tested here")

        print(port)
        print(proto)
        print(name)
        print("-" * 60)



if __name__ == "__main__":
    main()
