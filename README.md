🚀 Enterprise Infrastructure & IP Resource Management System
A web-based Infrastructure Management System built using **Python (Streamlit)** and **SQLite** to manage IP allocation, VM provisioning, and server resource utilization efficiently.

 📌 Project Overview
This system automates the process of managing IP addresses, allocating virtual machines (VMs), and monitoring server resources. It replaces manual tracking with a smart, centralized solution.

 🎯 Features
- ✅ IP Pool Management (Free & Assigned IPs)
- ✅ VM Creation & Resource Allocation
- ✅ Smart Server Selection Algorithm
- ✅ CSV Bulk Import for Infrastructure Data
- ✅ Real-time Dashboard Analytics
- ✅ Audit Logging System
- ✅ Server Capacity Monitoring
  
 🧠 Smart Server Selection
The system automatically selects the best server based on:
- Available CPU
- Available RAM
- Available Storage
This ensures **load balancing** and prevents server overload.

## 🏗️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Python  
- **Database:** SQLite  
- **Libraries:** Pandas, IPAddress  

⚙️ How It Works
1. User logs into the system  
2. Imports CSV or creates VM manually  
3. System validates and stores data  
4. Server capacity is checked  
5. Best server is selected automatically  
6. IP is assigned to VM  
7. Dashboard updates in real-time
   
📂 Database Structure
- `ip_pool` → Stores all IP addresses  
- `servers` → Stores server details  
- `vm_requests` → Stores VM allocations  
- `audit_log` → Tracks system actions
  
📸 Screenshots
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/70b54e76-27cc-4afa-ae86-1148bceca526" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d58b85d0-bc4e-49bc-8a40-9c1c213bcb5b" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/e381652e-74e8-4c15-9c7c-a8f5d971d9b6" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/57290065-2e5c-4b52-80a5-da0b30c29a9b" />
<img width="1919" height="631" alt="image" src="https://github.com/user-attachments/assets/2abbcea5-6d56-4577-9aa3-81b5730fa685" />

 🚀 Installation & Setup
```bash
# Clone repository
git clone https://github.com/your-username/your-repo-name.git

# Navigate to project folder
cd your-repo-name

# Install dependenciespip install -r requirements.txt

# Run the application
streamlit run app.py
