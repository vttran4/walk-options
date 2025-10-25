# 💃 Options Optimizer

A **Streamlit web app** that helps you maximize your **options premium** while staying within your **collateral limit** — because smart investing can be as stylish as it is strategic 🎀  

---

## 🧠 Overview

The **Options Optimizer** allows you to:
- Upload or edit a table of stock options with **Stock, Collateral, and Premium** values.  
- Define your **total available collateral**.  
- Automatically calculate the **optimal number of contracts** to maximize your total premium using **linear programming**.  

Behind the scenes, it uses [PuLP](https://coin-or.github.io/pulp/) to solve the optimization problem with an integer linear programming model.

---

## ⚙️ Tech Stack

- 🐍 **Python 3.9+**
- 📊 **Streamlit** – Interactive web UI
- 🧮 **Pandas** – Data management
- 💪 **PuLP** – Linear optimization solver
- 📘 **OpenPyXL** – Excel file reader

---

## 🚀 Setup & Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/vttran4/walk-options.git
   cd walk-options


2. **Create and activate a virtual environment**


   python -m venv venv
   
   source venv/bin/activate      # On macOS/Linux
   
   venv\Scripts\activate         # On Windows


4. **pip install -r requirements.txt**

5. **Run the app**

   streamlit run app.py
