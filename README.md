# 🔷 ARP Handling in SDN using POX Controller

## 📌 Project Overview

This project implements **ARP (Address Resolution Protocol) handling** in a **Software Defined Network (SDN)** using the **POX controller** and **Mininet**.

In traditional networks, ARP requests are broadcast to all devices, leading to unnecessary network traffic. This project demonstrates how a centralized SDN controller can efficiently manage ARP requests and responses, reducing flooding and improving performance.

---

## 🎯 Objectives

* Intercept ARP packets at the controller
* Generate ARP replies centrally
* Perform host discovery (IP–MAC mapping)
* Validate communication between hosts

---

## 🏗️ System Architecture

* **Mininet** → Creates virtual network (hosts & switches)
* **POX Controller** → Handles ARP logic (control plane)
* **Switch (s1)** → Forwards packets (data plane)
* **Hosts (h1–h4)** → End devices

---

## ⚙️ Working Principle

1. A host sends an ARP request (e.g., *Who has 10.0.0.2?*)
2. The switch forwards the packet to the controller
3. The controller intercepts the ARP packet
4. It stores host information (IP, MAC, Port)
5. If destination is known → controller sends ARP reply
6. If unknown → packet is flooded
7. Communication is established between hosts

---

## 🔍 Key Features

* ✔️ Centralized ARP handling using SDN
* ✔️ Reduced network flooding
* ✔️ Dynamic host discovery
* ✔️ Efficient packet processing
* ✔️ Successful communication with 0% packet loss

---

## 📁 Project Files

* `arp_handler.py` → POX controller logic for ARP handling
* `custom_topo.py` → Mininet topology script

---

## 🛠️ Technologies Used

* Python
* Mininet
* POX Controller
* OpenFlow Protocol

---

## 📊 Output

* ARP requests intercepted by controller
* ARP replies generated centrally
* Hosts discovered dynamically
* Successful ping communication between all hosts

---

## 🚀 Conclusion

This project demonstrates how SDN can optimize traditional network operations by centralizing ARP handling. It reduces unnecessary broadcast traffic and improves overall network efficiency.

---

## 👤 Author

* GitHub: mounika-200622
