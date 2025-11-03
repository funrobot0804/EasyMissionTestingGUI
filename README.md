# 🚗 AMR Dispatch System (Web-based)

A **web-based AMR (Autonomous Mobile Robot) dispatching system** implemented in **Python**,  
using the **FMS RESTful API provided by MSI AMR**.  
It provides functionality similar to **Uber**, allowing general operators to request AMR services via a web interface.

---

## 🌟 Features

- 📡 Integration with **MSI AMR FMS RESTful API**
- 🌍 Web-based interface for calling and managing AMR vehicles
- 🚘 AMR status and location monitoring
- 📅 Task scheduling and history tracking
- 🧭 Real-time job progress visualization
- 🔒 Authentication and access control (optional)

---

## 🧰 System Architecture
+------------------+ +-------------------------+
| Web Frontend | <------> | Python Backend (API) |
| (Flask / FastAPI)| | Uses MSI FMS REST API |
+------------------+ +-----------+-------------+
|
v
+----------------+
| FMS Server |
| (MSI AMR Core) |
+----------------+



## Install dependencies
pip install fastapi uvicorn jinja2



## Run the web server
uvicorn main:app --reload --host 0.0.0.0 --port 8000


## Open your browser (If your FMS and this program run in same PC)
http://127.0.0.1:8000/?station=P1
