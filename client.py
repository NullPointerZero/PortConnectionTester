
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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(timeout)
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
            ok, latency, info = test_udp(host, port, timeout)
        elif (proto == "tcp"):
            ## TODO TCP Testfunction
            print("tcp will be tested here")
            continue
        else:
            print(f"unbekanntes Protokoll in Config: {proto} (Port {port})")
            continue

        print(port)
        print(proto)
        print(name)
        print("-" * 60)

        results.append({
            "name" : name,
            "port" : port,
            "protocol" : proto,
            "ok" : ok,
            "latency" : latency,
            "info" : info
        })

        print("\nErgebnisübersicht")
        print("-" * 60)
        print(f"{'Name':25} {'Proto':5} {'Port':5} {'Status':8} {'Latenz [ms]':12} Info")

        for r in results:
            status = "OK" if r["ok"] else "FAIL"
            latency = f"{r['latency']: .1f}" if r["latency"] is not None else "-"
            print(f"{r['name'][:25]:25} {r['protocol'].upper():5} {r['port']:5} {status:8} {latency:12} {r['info']}")


if __name__ == "__main__":
    main()
