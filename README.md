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
- ✅ **Pytest** – Tests

---

## ✅ Phase 1 Highlights (Portfolio-Ready)

- Clear separation of UI and core optimization logic
- Input validation with helpful errors
- Unit tests for reliability
- Simple, reproducible setup
- Tests passing locally: `python3 -m pytest -q` (Feb 4, 2026)

---

## ✅ Phase 2 Highlights (API + UI Split)

- FastAPI backend with `/optimize` endpoint
- Streamlit frontend calls the API
- Clean interface for future scaling/deployment

---

## 🚀 Setup & Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/vttran4/walk-options.git
   cd walk-options
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On macOS/Linux
   venv\\Scripts\\activate         # On Windows
   ```

3. **Install required python packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Run tests**
   ```bash
   pytest
   ```

---

## 🔌 Phase 2: Run API + UI

1. **Start the API**
   ```bash
   uvicorn api:app --reload
   ```

2. **Start the UI (in another terminal)**
   ```bash
   streamlit run app.py
   ```

3. **Optional: Set API URL**
   ```bash
   export OPTIMIZER_API_URL="http://127.0.0.1:8000"
   ```

4. **One-command dev start**
   ```bash
   ./scripts/run-dev.sh
   ```

---

## 📁 Project Structure

```
core/
  optimizer.py        # Optimization logic (PuLP)
  validation.py       # Input checks
tests/
  test_optimizer.py   # Unit tests
app.py                # Streamlit UI
api.py                # FastAPI backend
```
