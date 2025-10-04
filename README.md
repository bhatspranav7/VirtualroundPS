# 💼 Expense Approval System

## 📌 Overview
Companies often struggle with manual expense reimbursement processes that are time-consuming, error-prone, and lack transparency.  
This project is a **smart Expense Management & Approval System** that allows employees to submit expenses and managers/admins to approve them through **multi-level workflows** with **conditional rules**.

Built in **1 day hackathon** (virtual round).

---

## 🎯 Core Features
- **Authentication & Role Management**
  - Roles: **Admin, Manager, Employee**
  - Admin can create employees/managers and assign roles

- **Expense Submission (Employee)**
  - Submit expense claims (amount, category, description, date, receipt upload)
  - Multi-currency support (converted to company’s default currency)
  - View personal expense history (approved/rejected)

- **Approval Workflow (Manager/Admin)**
  - Sequential approvals: Manager → Finance → Director
  - Conditional rules:
    - ✅ Percentage rule (e.g., 60% approvals = approved)
    - ✅ Specific approver rule (e.g., CFO auto-approves)
    - ✅ Hybrid rule (e.g., 60% OR CFO approval)

- **Extra Features**
  - OCR Receipt Scanning (auto-extract amount/date/vendor)
  - Real-time currency conversion using [Exchangerate API](https://api.exchangerate-api.com/)

---

## 🏗️ Tech Stack
**Frontend**
- React + TailwindCSS  

**Backend**
- FastAPI (Python) / Express (Node.js)  
- REST APIs for auth, expense submission, approval workflow  

**Database**
- SQLite (for hackathon speed, easy to switch to PostgreSQL)  

**APIs**
- Country & Currency: [REST Countries](https://restcountries.com/)  
- Currency Conversion: [Exchangerate API](https://api.exchangerate-api.com/)  

---

## 📂 Project Structure
expense-approval-system/
│
├── backend/ # API + workflow engine
│ ├── app/
│ │ ├── main.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── routes/
│ │ └── services/
│ └── requirements.txt
│
├── frontend/ # React + Tailwind
│ ├── src/
│ │ ├── components/
│ │ └── pages/
│ └── package.json
│
├── docs/ # Hackathon docs
│ ├── architecture.png
│ └── demo-script.md
│
├── README.md
└── docker-compose.yml