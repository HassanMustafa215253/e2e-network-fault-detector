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

### Python Dependencies
Install required Python packages using:

```bash
pip install -r requirements.txt
