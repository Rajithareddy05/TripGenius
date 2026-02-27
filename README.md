# 🧳 AI-Powered Travel Itinerary Planner
**TripGenius

An AI-driven web application built with **Flask**, **LangChain**, and **Groq** to generate intelligent, personalized travel itineraries. Users can input preferences, upload images, and manage trips effortlessly.

---

## 🚀 Overview

Plan your dream trip with the power of AI! This app takes your inputs — destination, interests, group type, budget, and transport — and generates:

- ✍️ **Trip Summary**
- 🗓️ **Daily Itinerary** with activities, timings, and cost estimates
- 🍽️ **Food Recommendations**
- 🌍 **Hidden Gems**
- 💰 **Detailed Cost Breakdown**

---

## 🔥 Features

| Feature | Description |
|--------|-------------|
| 🧠 **AI-Powered Planning** | Uses **LLaMA-3-70B** via **Groq API** for itinerary generation |
| 📤 **Photo Uploads** | Upload reference images for your trip |
| 💾 **Save, Edit, Delete Trips** | Full trip management using session storage |
| 📅 **Multi-Day Itinerary Support** | Plan trips from 1 to N days |
| 🎨 **User-Friendly Interface** | Built with Flask & Jinja templating |
| 💬 **Contact & About Pages** | Extra user interaction pages |

---

## ⚙️ Tech Stack

| Technology | Description |
|------------|-------------|
| **Python + Flask** | Backend and server logic |
| **HTML/CSS + Jinja2** | Frontend templating and UI |
| **LangChain** | Prompt orchestration and formatting |
| **Groq API** | LLM backend (LLaMA 3-70B) |
| **dotenv** | Secure API key management |
| **Werkzeug** | File handling and security |
| **Jinja2 Filters** | Custom date formatting for templates |

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository

    git clone https://github.com/yourusername/AI-Powered-Travel-Itinerary-Planner.git
    cd AI-Powered-Travel-Itinerary-Planner


### 2️⃣ Create Virtual Environment

    python -m venv venv
    venv\Scripts\activate

### 3️⃣  Configure Environment Variables
Create a .env file in the root directory:

    GROQ_API_KEY=your_groq_api_key
    SECRET_KEY=your_flask_secret_key

### 5️⃣ Run the App

    python app.py

Then open your browser and navigate to:

    http://127.0.0.1:5000

---

## 📸 Screenshots

<img width="1893" height="943" alt="Screenshot 2025-08-06 155149" src="https://github.com/user-attachments/assets/58401fba-f060-40fe-8003-020d70729a2e" />

<img width="1890" height="934" alt="Screenshot 2025-08-06 155212" src="https://github.com/user-attachments/assets/9fb4780b-d0ee-4c94-9fda-b0272853edad" />

<img width="982" height="871" alt="Screenshot 2025-08-06 161154" src="https://github.com/user-attachments/assets/0315dd21-b147-49a3-98a1-def978d79bb9" />

<img width="966" height="593" alt="Screenshot 2025-08-06 161214" src="https://github.com/user-attachments/assets/d071ec06-ddc2-402b-8f7c-097f86161137" />

<img width="1062" height="281" alt="Screenshot 2025-08-06 161225" src="https://github.com/user-attachments/assets/14d83547-3441-4045-9de5-c177140f3036" />

<img width="967" height="692" alt="Screenshot 2025-08-06 161235" src="https://github.com/user-attachments/assets/08f36398-62a9-42d5-9809-7594ae6e3afc" />

---



