# 🧼 GA Cleaning Service

A **Streamlit** app to manage, calculate, and track cleaning service jobs, integrated with **Google Sheets** for real-time data.

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Workflow](#example-workflow)
- [Project Structure](#project-structure)
- [Reference](#reference)

---

## ✨ Features

- Google Authentication (only whitelisted users can log in)
- Dynamic Pricing (based on product type and conditions)
- Google Sheets Integration (reads and updates records)
- Session Persistence (keeps user selections)
- Custom Layout Display (shows cleaning steps per product)

---

## ⚙️ Installation

1. **Clone the repository**
```toml
git clone https://github.com/your-org/ga-cleaning-service.git

cd ga-cleaning-service
```

2. **Install dependencies**
```pip install -r requirements.txt```

3. **Create** ```secrets.toml```
```toml
[connections.gsheets]
email = "your_service_account_email"
private_key = "-----BEGIN PRIVATE KEY-----\n..."

[allowed_users]
emails = ["user1@example.com", "user2@example.com"]
```

4. **Run the app**

## ⚙️ Configuration

- **Google Sheets Connection**
- Make sure your service account has editor access to your Google Sheets.

- **Allowed Users**
- Only emails listed in `[allowed_users]` are permitted.

---

## 🛠️ Usage

1. **Login**
- Sign in with Google.
- Unauthorized users will be denied.

2. **Select Customer**
- Choose a customer with `ON PROGRESS` status.

3. **Select Product**
- Pick the product.
- If required, enter the multiplier (e.g., area in square meters).

4. **Rate the Condition**
- Four criteria:
  - Skala Kekotoran
  - Tahap Kekotoran
  - Kondisi Barang
  - Masa Siap Service

5. **Apply Discounts**
- Select discount amount if needed.

6. **Save Record**
- Click **Save cleaning records** to update Google Sheets.

---

## 💡 Example Workflow

**Scenario:**

- Customer: Ali Furniture
- Product: CARPET
- Multiplier: 5
- Ratings:
- Skala Kekotoran: 2
- Tahap Kekotoran: LEVEL 3
- Kondisi Barang: GRED B
- Masa Siap: 2 JAM - 4 JAM
- Discount: RM5

**Daily Habit Example:**

- After every cleaning job:
- Open the app.
- Select customer and product.
- Enter multiplier and condition ratings.
- Save the record before leaving.

---

## 📂 Project Structure
```toml
ga-cleaning-service/
├── app.py # Main application script
├── requirements.txt # Dependency list
└── README.md # This README file
```

---

## 📚 Reference

- [Streamlit Documentation](https://docs.streamlit.io)
- [streamlit_gsheets](https://github.com/streamlit/streamlit-gsheets)
- [Google Sheets API](https://developers.google.com/sheets/api)

---
