import requests
from collections import deque
import telnetlib
import time
import re
import argparse
from gns3fy import Gns3Connector

GNS3_SERVER = "http://localhost:3080"


SOURCE_NODE = "PC1"
DEST_NODE = "PC5"


# FIND PROJECT

def find_project(connector, project_name):
    projects = connector.get_projects()
    for p in projects:
        if p['name'] == project_name or p['project_id'] == project_name:
            return p
    raise RuntimeError(f'Project "{project_name}" not found on server {connector.base_url}')



# FETCH TOPOLOGY

def get_nodes(PROJECT_ID):
    url = f"{GNS3_SERVER}/v2/projects/{PROJECT_ID}/nodes"
    return {n["name"]: n for n in requests.get(url).json()}


def get_links(PROJECT_ID):
    url = f"{GNS3_SERVER}/v2/projects/{PROJECT_ID}/links"
    return requests.get(url).json()


def build_graph(nodes, links):
    graph = {name: [] for name in nodes}

    for link in links:
        if len(link["nodes"]) != 2:
            continue

        a = link["nodes"][0]["node_id"]
        b = link["nodes"][1]["node_id"]

        n1 = next(k for k, v in nodes.items() if v["node_id"] == a)
        n2 = next(k for k, v in nodes.items() if v["node_id"] == b)

        graph[n1].append(n2)
        graph[n2].append(n1)

    return graph


def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None



# LOW-LEVEL TELNET 
def telnet_send(host, port, cmd, expect=b">", wait=0.5):
    try:
        tn = telnetlib.Telnet(host, port, timeout=3)
        tn.write(b"\n")
        time.sleep(wait)
        tn.write(cmd + b"\n")
        time.sleep(wait)
        output = tn.read_very_eager().decode(errors="ignore")
        tn.close()
        return True, output
    except:
        return False, ""



# IP CHECKING
def extract_ips_from_router(output):
    """
    Parses output of 'show ip interface brief'.
    Returns list of IPs.
    """
    ips = re.findall(r"\d+\.\d+\.\d+\.\d+", output)
    return ips


def extract_vpcs_ip_and_gateway(output):
    """
    Parses VPCS 'show ip' output.
    Returns:
      ip, gateway
    """
    ip_match = re.search(r"IP/MASK\s*:\s*(\d+\.\d+\.\d+\.\d+)", output)
    gw_match = re.search(r"GATEWAY\s*:\s*(\d+\.\d+\.\d+\.\d+)", output)

    ip = ip_match.group(1) if ip_match else None
    gw = gw_match.group(1) if gw_match else None
    return ip, gw



# NODE TESTING
def test_router(node):
    host = node["console_host"]
    port = node["console"]

    ok, out = telnet_send(host, port, b"show ip interface brief")
    
    if not ok:
        return False, "Router console unreachable"

    ips = extract_ips_from_router(out)
    if not ips:
        return False, "Router has NO IP configured"

    return True, ""


def test_vpcs(node):
    host = node["console_host"]
    port = node["console"]

    ok, out = telnet_send(host, port, b"show ip", expect=b">")
    if not ok:
        return False, "VPCS console unreachable"
    
    ip, gw = extract_vpcs_ip_and_gateway(out)

    
    if not ip or ip == "0.0.0.0":
        return False, "VPCS has NO IP configured"

    if not gw or gw == "0.0.0.0":
        return False, "VPCS has NO gateway configured"

    return True, ""


def test_node(node):
    if node["status"] != "started":
        return False, "Node is powered OFF"

    ntype = node["node_type"]

    if ntype == "vpcs":
        return test_vpcs(node)

    elif ntype in ("dynamips", "iou"):
        return test_router(node)

    return True, "Node ignored (no IP checks available)"



# PATH CHECKER
def check_path(path, nodes):
    print("Checking path:", " → ".join(path))
    print()

    for name in path:
        node = nodes[name]
        ok, msg = test_node(node)

        status = "✔ OK" if ok else "❌ ERROR"
        print(f"{name}: {status} — {msg}")

        if not ok:
            print(f"\n🔴 FAILURE at: {name}")
            return False

    print("\n🟢 Path healthy end-to-end!")
    return True




def main():
    
    ap = argparse.ArgumentParser(description='GNS3 backtrace diagnostic script')
    ap.add_argument('--gns3', default='http://127.0.0.1:3080', help='GNS3 server URL')
    ap.add_argument('--project', required=True, help='Project name or id')
    ap.add_argument('--source', required=True, help='Source IP that reported the error')
    ap.add_argument('--dest', required=True, help='Destination IP that failed to respond')
    ap.add_argument('--timeout', type=int, default=12, help='Traceroute timeout seconds')
    args = ap.parse_args()

    # Connect to GNS3
    server = Gns3Connector(url=args.gns3)
    print(f"Connected to GNS3 server at {args.gns3}")
    
    project = find_project(server, args.project)
    project_id = project['project_id']
    print(f"Using project: {project['name']} (id {project_id})")
    
    
    nodes = get_nodes(project_id)
    links = get_links(project_id)

    graph = build_graph(nodes, links)

    path = bfs_path(graph, SOURCE_NODE, DEST_NODE)
    if not path:
        print("No path found between nodes!")
        return

    print("Path found:", " → ".join(path))
    print()
    check_path(path, nodes)


if __name__ == "__main__":
    main()
