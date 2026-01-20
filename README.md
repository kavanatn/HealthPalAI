# HealthPal 🌿💙

<div align="center">

<div align="center">
  <img src=https://github.com/user-attachments/assets/1c0cc86a-1a02-4e67-b069-c33d6d652587 alt="HealthPal Logo" width="150" height="150">
</div>

**Your AI-Powered Health Companion**


</div>

## 📌 Overview

HealthPal is an intelligent healthcare application designed to track, monitor, and enhance personal health. By leveraging AI-driven recommendations and user data, HealthPal provides personalized insights into various health aspects, including sleep, weight changes, mood tracking, and activity monitoring.

HealthPal uses **Mistral AI** to generate personalized health advice based on user-input data. The data is collected via a dynamic **Health Questionnaire**, and the generated insights are stored in a database until a new recommendation is requested. Additionally, **HealthPal AI Chatbot** is integrated to offer real-time health guidance and answer health-related queries.

The platform allows users to monitor their health progress through a comprehensive **Dashboard**, update their health records, and receive instant health insights from the AI Chatbot.

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
- 🩺 **Health Guidance**: Offers guidance on health conditions, fitness, and nutrition.
- 💊 **Medication Advice**: Provides general medication and supplement recommendations.
- 🍎 **Diet & Nutrition**: Suggests balanced diets and meal plans.
- 💤 **Sleep Advice**: Offers tips to improve sleep quality.
- 💻 **24/7 Availability**: Available anytime for user queries.

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

1. **User Registration**: Users sign up/sign in securely.
2. **Health Questionnaire**: Users fill out a dynamic health questionnaire providing relevant health data.
3. **AI Recommendations**: Collected data is sent to **Mistral AI API** for personalized health recommendations.
4. **Dashboard Access**: Users access a dashboard displaying their health progress and insights.
5. **Health Records Management**: Users can update and maintain their health records.
6. **AI Chatbot Interaction**: Users can chat with the AI Chatbot for real-time health advice and recommendations.
7. **Recommendation History**: Recommendations are stored in the database until a new one is requested.
8. **Blogs Section**: Users can explore health-related articles and tips.

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

1. Go to the **Chatbot Section** in the navigation bar.
2. Enter your health-related query in the chat input.
3. The AI Chatbot will generate a response based on your query.
4. You can ask about:
   - **Diet Plans**
   - **Workout Routines**
   - **Sleep Patterns**
   - **Medication Advice**
   - **General Health Queries**

---

## 💡 Future Enhancements

- 📊 **Integration with Wearable Devices** for real-time health tracking.
- 📈 **Advanced Data Analytics** for better health insights.
- 📲 **Mobile App** to enhance user accessibility.
- 👥 **Community Forum** for health discussions.
- 🤖 **Voice Assistant Support** for the AI Chatbot.

---

### ⭐ HealthPal 🌿💙 – Your AI Health Companion! 🚀💙
