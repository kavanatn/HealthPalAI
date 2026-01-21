# HealthPal 🌿💙

<div align="center">

<div align="center">
  <img src=https://github.com/user-attachments/assets/1c0cc86a-1a02-4e67-b069-c33d6d652587 alt="HealthPal Logo" width="150" height="150">
</div>

**Your AI-Powered Health Companion**


</div>

## 📌 Overview

HealthPal is an intelligent healthcare application designed to track, monitor, and enhance personal health. By leveraging AI-driven recommendations and structured user data, HealthPal provides personalized insights into key health aspects such as **sleep, weight changes, mood tracking, and activity monitoring**.

HealthPal uses **Mistral AI** to generate personalized health advice based on user-input data collected through a dynamic **Health Questionnaire**. Generated insights are securely stored in a database and refreshed whenever new recommendations are requested.

The platform features a comprehensive **Dashboard** for progress tracking and an integrated **AI Chatbot** that offers real-time health guidance and answers health-related queries.

---

## ❓ Why HealthPal?

Personal health data is often scattered across multiple tools and tracked inconsistently. HealthPal centralizes health inputs and applies AI to transform raw data into **meaningful, personalized insights**.

This project focuses on:
- Practical AI integration beyond basic chatbot use cases
- Secure handling of sensitive user data
- Building a scalable, full-stack health application with real-world relevance

---

## 🚀 Features

- 🔐 **User Authentication**: Secure sign-up and sign-in.
- 📝 **Health Questionnaire**: Collects user health data.
- 🤖 **AI Recommendations**: Provides personalized health advice using Mistral AI.
- 📊 **Health Tracking**: Monitors weight, sleep, activity, and mood changes.
- 💾 **Health Records**: Stores and updates user health data.
- 📋 **Dashboard**: Displays health progress and insights.
- 💬 **AI Chatbot**: Real-time health guidance and instant responses to health queries.
- 📰 **Blogs Section**: Offers health-related articles and tips.
- ⚙️ **Settings**: Allows customization of user preferences.

---

## 💬 AI Chatbot Integration

The **HealthPal AI Chatbot** is designed to provide real-time health insights and answer health-related queries instantly.

**Capabilities of HealthPal AI Chatbot:**
- 🩺 General health, fitness, and wellness guidance
- 💊 Medication and supplement information (general guidance)
- 🍎 Diet and nutrition suggestions
- 💤 Sleep improvement tips
- 💻 24/7 availability for user queries

The chatbot utilizes **Mistral AI** to understand user inputs and generate appropriate health recommendations.

---

## 🏗️ Technology Stack

<div align="center">

### Frontend
[![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### Backend
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

### Database
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)


### AI Integration
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-1B1C1D?style=for-the-badge&logoColor=white)](https://mistral.ai/)

</div>

---

## 📊 User Flow

1. User Registration / Login  
2. Health Questionnaire Submission  
3. AI Recommendation Generation (Mistral AI API)  
4. Dashboard Access & Health Metrics Visualization  
5. Health Records Management  
6. AI Chatbot Interaction  
7. Recommendation History Storage  
8. Blogs & Health Resources Access  

---

## 💻 Application Screenshots

### Login 
![Image](https://github.com/user-attachments/assets/6260d380-1db6-40ce-861a-c54205225977)

### Dashboard: Health Metrics Visualization
![Image](https://github.com/user-attachments/assets/b2d43f65-13db-4011-a44e-ae19bf847418)


### AI Chatbot Interface
![Image](https://github.com/user-attachments/assets/4c2f4dce-641b-419c-a758-105aeb0dc9e0)


### Recommendations 
![Image](https://github.com/user-attachments/assets/31eb0f33-a8f9-4b14-91e7-7527c5b4dee3)

### Blogs
![Image](https://github.com/user-attachments/assets/eec0c29e-5568-4cec-914f-3d76a21c3a5d)

### Profile settings
![Image](https://github.com/user-attachments/assets/db7db331-89d1-4cdd-8fb9-3f5645f70bd1)


---

## 🛠️ Setup & Installation


1. **Clone the repository**:
```bash
git clone https://github.com/kavanatn/HealthPalAI.git
```

2. **Navigate to the project directory**:
```bash
cd HealthPalAI-main
```

3. **Set up Python Environment (optional but recommended)**:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**:
```bash
# Copy the example environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac
```

6. **Add your Mistral AI API key**:
   - Open the `.env` file
   - Replace `your-mistral-api-key-here` with your actual Mistral AI API key
   - (Optional) Generate a secure SECRET_KEY:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```

7. **Run the Flask application**:
```bash
python app.py
```

8. **Access the application**:
   - Open http://localhost:5000 in your browser.

**Security Note**: Your API keys are now safely stored in the `.env` file, which is automatically excluded from Git commits.

---

## 💬 How to Use the AI Chatbot

1. Navigate to the Chatbot section.
2. Enter your health-related query.
3. Receive AI-generated guidance instantly.
4. Supported queries include:
   - **Diet Plans**
   - **Workout Routines**
   - **Sleep Patterns**
   - **Medication Advice**
   - **General Health Queries**

---
## ⚠️ Disclaimer

HealthPal is an educational and experimental project.
AI-generated insights are not a substitute for professional medical advice.
Users should consult qualified healthcare professionals for medical decisions.

---
## 💡 Future Enhancements

- 📊 **Integration with Wearable Devices** for real-time health tracking.
- 📈 **Advanced Data Analytics** for better health insights.
- 📲 **Mobile App** to enhance user accessibility.
- 👥 **Community Forum** for health discussions.
- 🤖 **Voice Assistant Support** for the AI Chatbot.

---

### ⭐ HealthPal 🌿💙 – Your AI Health Companion! 🚀💙
