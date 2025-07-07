# 🧼 GA Cleaning Service

A **Streamlit** app to manage, calculate, and track cleaning service jobs, integrated with **Google Sheets** for real-time data storage.

[👉 **Access the Live App Here**](https://ga-cleaning-service.streamlit.app/)

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

- **Google Authentication**  
  Only whitelisted users can log in.
- **Dynamic Pricing**  
  Pricing adjusts based on:
  - Product type
  - Dirt level
  - Condition
  - Service duration
- **Google Sheets Integration**  
  Reads settings, current records, and writes completed jobs.
- **Session Persistence**  
  Keeps user selections during the session.
- **Custom Layout Display**  
  Shows cleaning steps depending on the product type.

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ga-cleaning-service.git

   cd ga-cleaning-service
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create** `.streamlit/secrets.toml`

   ```toml
   [gsheets]
   credentials = "<YOUR GOOGLE SERVICE ACCOUNT JSON>"
   spreadsheet = "<YOUR GOOGLE SHEET URL>"

   [allowed_users]
   emails = ["user1@example.com", "user2@example.com"]
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## ⚙️ Configuration

* **Google Sheets Connection**

  * Your service account must have Editor access to the Google Sheet.
  * The spreadsheet must contain these worksheets:

    * `SETTING`
    * `RECORDS`
    * `CLEANING RECORDS`

* **Allowed Users**

  * Only emails listed under `[allowed_users]` are permitted to access.

---

## 🛠️ Usage

1. **Login**

   * Sign in with Google.
   * Unauthorized users will see an error and be logged out.

2. **Select Customer**

   * Choose a customer with `ON PROGRESS` status.

3. **Select Product**

   * Pick a product to clean.
   * If required, enter the multiplier (e.g., carpet size).

4. **Rate the Condition**

   * Four rating categories:

     * Skala Kekotoran
     * Tahap Kekotoran
     * Kondisi Barang
     * Masa Siap Service

5. **Apply Discount**

   * Select RM discount if applicable.

6. **Save Record**

   * Click **Save cleaning records** to update the `CLEANING RECORDS` worksheet.

---

## 💡 Example Workflow

**Scenario:**

* **Customer:** Ali Furniture
* **Product:** CARPET
* **Multiplier:** 5
* **Ratings:**

  * Skala Kekotoran: 2
  * Tahap Kekotoran: LEVEL 3
  * Kondisi Barang: GRED B
  * Masa Siap Service: 2 JAM - 4 JAM
* **Discount:** RM5

**Daily Habit Example:**

* After each cleaning job:

  * Open the app.
  * Select customer and product.
  * Enter the multiplier and ratings.
  * Save the record before leaving the site.

---

## 📂 Project Structure

```bash
ga-cleaning-service/
├── app.py                # Main Streamlit application script
├── requirements.txt      # List of dependencies
└── README.md             # This README file
```

---

## 📚 Reference

* [Streamlit Documentation](https://docs.streamlit.io)
* [streamlit\_gsheets](https://github.com/streamlit/streamlit-gsheets)
* [Google Sheets API](https://developers.google.com/sheets/api)
* [👉 Access the GA Cleaning Service App](https://ga-cleaning-service.streamlit.app/)

