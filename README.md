# End-to-End Link Monitoring & Diagnostics Tool

This project is an **real time end-to-end network link monitoring and diagnostics system** that detects connectivity failures between two client endpoints, identifies **why a link broke**, and maps failures onto a **graph representation of a GNS3-managed network topology**.

The system operates on virtual network environments created using **GNS3**, enabling realistic testing, monitoring, and fault analysis of network paths in real time.

---

## 🚀 Features

- Detects end-to-end connectivity failures between two clients
- Identifies and reports the **cause of link breakage** (e.g. interface down, routing issues, packet loss)
- Integrates directly with **GNS3** via its API
- Builds a **graph-based representation** of the GNS3 topology
- Maps detected failures to specific nodes or links
- Supports automated diagnostics using Telnet-based device access
- Every thing happens in real time

---

## 🛠️ Technologies Used

- **Python 3.8+**
- GNS3
- `gns3fy` (GNS3 API interaction)
- `requests` (HTTP communication)
- Python standard networking and utility libraries

---

## 📦 Requirements

### Software
- Python 3.8 or higher
- GNS3 (local or cloud-based server)
- Network devices in GNS3 with Telnet enabled

### ⚙️ GNS3 Configuration

Preferred Setup (Recommended)
It is recommended to use your own GNS3 architecture, especially for custom topologies or advanced testing.
If you are using a cloud-based or remote GNS3 server, update the following variable in the main script:
GNS3_SERVER = "http://<your-gns3-server>"
Replace <your-gns3-server> with the IP address or hostname of your GNS3 server.
GNS3 may also run on local server; if using localserver then GNS_SERVER is already set to search local server

Default / Basic Architecture

For convenience, a basic GNS3 topology is already provided within the project but first the project should be loaded into localserver using GNS3.
This default setup can be used for:

Initial testing
Dmonstrations
Understanding the project workflow
Users may modify or replace this architecture as needed.

## 📊 Topology Graph Representation

The project constructs a graph model of the GNS3 topology, where:
Nodes represent network devices
Edges represent links between devices
This graph is used to:

Analyze end-to-end paths
Identify failure points
Visualize how errors propagate through the network

## ▶️ Usage

Start your GNS3 server
Ensure devices are reachable via Telnet
Configure the GNS3_SERVER variable if using a remote server
Run the main script:

python main.py


### Python Dependencies
Install required Python packages using:

pip install -r requirements.txt
