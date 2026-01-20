import os
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
import requests
import joblib
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash, check_password_hash
import json
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Use SQLite for now (or get from environment)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
# Use secure secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Stores session data on the server

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login page if not authenticated

# Define the user model


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    recommendations = db.relationship(
        'Recommendation', backref='user', lazy=True)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    sleep = db.Column(db.Float, nullable=False)
    physical_activity = db.Column(db.String(50), nullable=False)
    water_intake = db.Column(db.Float, nullable=False)
    diet = db.Column(db.String(100), nullable=False)
    chronic_conditions = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.String(100), nullable=False)
    smoking = db.Column(db.String(10), nullable=False)
    alcohol = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sleep_recommendation = db.Column(db.Text, nullable=False)
    diet_recommendation = db.Column(db.Text, nullable=False)
    exercise_recommendation = db.Column(db.Text, nullable=False)
    weight_management_recommendation = db.Column(db.Text, nullable=False)
    risk_prediction_recommendation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User loader function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create all tables
with app.app_context():
    db.create_all()
    print("Database tables created")

# Registration Form


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login Form


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Registration Route


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        # Handle errors if user exists
        if existing_user:
            if existing_user.username == form.username.data:
                flash("Username already taken. Please choose a different one.", "danger")
            elif existing_user.email == form.email.data:
                flash("Email already registered. Please login instead.", "danger")
            return redirect(url_for('register'))

        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    # If form has errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")

    return render_template('register.html', form=form)

# Login Route


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    # If form has errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")

    return render_template('login.html', form=form)


# Logout Route


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


CORS(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Mistral API Key from environment variable
mistral_api_key = os.getenv('MISTRAL_API_KEY')

if not mistral_api_key:
    print("WARNING: MISTRAL_API_KEY not found in environment variables!")
    print("Please add MISTRAL_API_KEY to your .env file")

# Home Route


@app.route("/")
def home():
    return render_template("index.html")

# Questionnaire Page


@app.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html")


@app.route('/dashboard')
@login_required
def dashboard():
    # Get the latest health record for the current user
    latest_record = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.created_at.desc()).first()

    if not latest_record:
        # No health records found
        return render_template('dashboard.html', has_health_records=False)

    # Calculate health metrics based on the latest record
    health_score = calculate_health_score(latest_record)
    activity_score = calculate_activity_score(latest_record)
    sleep_score = calculate_sleep_score(latest_record)
    mood_score = random.randint(70, 95)  # Placeholder for mood score

    # Calculate BMI
    height_m = latest_record.height / 100  # Convert cm to meters
    bmi = round(latest_record.weight / (height_m * height_m), 1)
    # Scale BMI to percentage (max 30)
    bmi_percentage = min(100, max(0, int((bmi / 30) * 100)))

    # Generate historical data for charts (last 7 days)
    date_labels = []
    health_data = []
    weight_data = []
    sleep_data = []
    activity_data = []
    mood_data = []

    # Get all records for the user, ordered by date
    all_records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.created_at.asc()).all()

    if len(all_records) >= 2:
        # Use actual historical data if available
        for record in all_records[-7:]:  # Get up to last 7 records
            date_labels.append(record.created_at.strftime('%b %d'))
            record_health_score = calculate_health_score(record)
            health_data.append(record_health_score)
            weight_data.append(record.weight)
            sleep_data.append(record.sleep)
            activity_data.append(calculate_activity_score(record))
            mood_data.append(random.randint(70, 95))  # Placeholder
    else:
        # Generate simulated historical data based on the latest record
        today = datetime.now()
        for i in range(7):
            day = today - timedelta(days=6-i)
            date_labels.append(day.strftime('%b %d'))

            # Add some random variation to the data
            variation = random.uniform(-0.05, 0.05)
            base_health = health_score * (1 + variation)
            health_data.append(round(base_health))

            weight_variation = random.uniform(-0.5, 0.5)
            weight_data.append(
                round(latest_record.weight + weight_variation, 1))

            sleep_variation = random.uniform(-0.5, 0.5)
            sleep_data.append(round(latest_record.sleep + sleep_variation, 1))

            activity_variation = random.uniform(-5, 5)
            activity_data.append(round(activity_score + activity_variation))

            mood_variation = random.uniform(-5, 5)
            mood_data.append(round(mood_score + mood_variation))

    return render_template(
        'dashboard.html',
        has_health_records=True,
        health_score=health_score,
        activity_score=activity_score,
        sleep_score=sleep_score,
        mood_score=mood_score,
        bmi=bmi,
        bmi_percentage=bmi_percentage,
        date_labels=date_labels,
        health_data=health_data,
        weight_data=weight_data,
        sleep_data=sleep_data,
        activity_data=activity_data,
        mood_data=mood_data,
        last_updated=latest_record.created_at.strftime('%B %d, %Y at %I:%M %p')
    )

# Helper functions for calculating health metrics


def calculate_health_score(record):
    # Calculate a health score based on various factors
    base_score = 70  # Start with a base score

    # Adjust based on BMI
    height_m = record.height / 100
    bmi = record.weight / (height_m * height_m)
    if 18.5 <= bmi <= 24.9:
        base_score += 10  # Ideal BMI
    elif 25 <= bmi <= 29.9 or 17 <= bmi < 18.5:
        base_score += 5   # Slightly overweight or underweight
    else:
        base_score -= 5   # Significantly overweight or underweight

    # Adjust based on sleep
    if 7 <= record.sleep <= 9:
        base_score += 5   # Ideal sleep
    elif 6 <= record.sleep < 7 or 9 < record.sleep <= 10:
        base_score += 2   # Slightly off ideal sleep
    else:
        base_score -= 3   # Poor sleep

    # Adjust based on physical activity
    if record.physical_activity == 'very-active':
        base_score += 10
    elif record.physical_activity == 'moderately-active':
        base_score += 7
    elif record.physical_activity == 'lightly-active':
        base_score += 3

    # Adjust based on smoking and alcohol
    if record.smoking == 'yes':
        base_score -= 10
    if record.alcohol == 'yes':
        base_score -= 5

    # Adjust based on chronic conditions
    if record.chronic_conditions != 'none' and record.chronic_conditions != 'None':
        base_score -= 5

    # Ensure score is between 0 and 100
    return max(0, min(100, base_score))


def calculate_activity_score(record):
    # Calculate activity score based on physical activity level
    base_score = 50

    if record.physical_activity == 'very-active':
        base_score = 90
    elif record.physical_activity == 'moderately-active':
        base_score = 75
    elif record.physical_activity == 'lightly-active':
        base_score = 60
    elif record.physical_activity == 'sedentary':
        base_score = 40

    # Add some variation
    variation = random.randint(-5, 5)
    return max(0, min(100, base_score + variation))


def calculate_sleep_score(record):
    # Calculate sleep score based on sleep hours
    ideal_sleep = 8  # Ideal sleep hours
    sleep_diff = abs(record.sleep - ideal_sleep)

    if sleep_diff <= 0.5:
        base_score = 90  # Very close to ideal
    elif sleep_diff <= 1:
        base_score = 80  # Slightly off
    elif sleep_diff <= 2:
        base_score = 70  # Moderately off
    else:
        base_score = 60  # Significantly off

    # Add some variation
    variation = random.randint(-5, 5)
    return max(0, min(100, base_score + variation))


@app.route('/api/dashboard_data')
@login_required
def dashboard_data():
    # Get the latest health record for the current user
    latest_record = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.created_at.desc()).first()

    if not latest_record:
        return jsonify({"error": "No health records found"}), 404

    # Calculate health metrics
    health_score = calculate_health_score(latest_record)
    activity_score = calculate_activity_score(latest_record)
    sleep_score = calculate_sleep_score(latest_record)
    mood_score = random.randint(70, 95)  # Placeholder for mood score

    # Calculate BMI
    height_m = latest_record.height / 100  # Convert cm to meters
    bmi = round(latest_record.weight / (height_m * height_m), 1)
    bmi_percentage = min(100, max(0, int((bmi / 30) * 100)))

    return jsonify({
        "health_score": health_score,
        "activity_score": activity_score,
        "sleep_score": sleep_score,
        "mood_score": mood_score,
        "bmi": bmi,
        "bmi_percentage": bmi_percentage,
        "last_updated": datetime.now().strftime('%B %d, %Y at %I:%M %p')
    })


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


@app.route('/healthrecords')
@login_required
def health_records():
    # Get all health records for the current user, ordered by creation date
    records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.created_at.desc()).all()
    return render_template('healthrecords.html', records=records)


@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    # Find the record
    record = HealthRecord.query.get_or_404(record_id)

    # Check if the record belongs to the current user
    if record.user_id != current_user.id:
        flash("You don't have permission to delete this record.", "danger")
        return redirect(url_for('health_records'))

    # Delete the record
    db.session.delete(record)
    db.session.commit()

    flash("Health record deleted successfully.", "success")
    return redirect(url_for('health_records'))


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')

    # Check if email already exists for another user
    existing_user = User.query.filter(
        User.email == email, User.id != current_user.id).first()
    if existing_user:
        flash("Email already in use by another account.", "danger")
        return redirect(url_for('settings'))

    # Update user information
    current_user.username = username
    current_user.email = email
    db.session.commit()

    flash("Profile updated successfully!", "success")
    return redirect(url_for('settings'))


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Check if current password is correct
    if not current_user.check_password(current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for('settings'))

    # Check if new passwords match
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('settings'))

    # Update password
    current_user.set_password(new_password)
    db.session.commit()

    flash("Password changed successfully!", "success")
    return redirect(url_for('settings'))


# Input sanitization function
def sanitize_input(text, max_length=500):
    """Sanitize user input to prevent prompt injection and limit length"""
    if not text:
        return ""
    
    # Remove any potential command injections or malicious patterns
    text = str(text).strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove multiple consecutive spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove any potential script tags or HTML
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove control characters except newlines and tabs
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    return text


@app.route("/chatbot/ask", methods=["POST"])
@limiter.limit("10 per minute")
def chatbot_ask():
    # Check if API key is configured
    if not mistral_api_key:
        return jsonify({"error": "AI service not configured. Please contact administrator."}), 503
    
    data = request.json
    user_message = data.get("message", "")
    
    # Sanitize user input
    user_message = sanitize_input(user_message, max_length=500)
    
    # Validate message is not empty after sanitization
    if not user_message or len(user_message.strip()) < 2:
        return jsonify({"error": "Please provide a valid message."}), 400

    system_message = """
    You are HealthPal, an AI health and wellness assistant. Your goal is to provide concise, structured, and interactive health guidance.

Response Guidelines:

Keep responses brief and clear (preferably under 5 sentences).
Use bullet points for readability.
Ask follow-up questions when needed to personalize advice.
Provide actionable recommendations (e.g., “Try drinking ginger tea” instead of lengthy explanations).
For serious health concerns, advise consulting a doctor.
Example Response Format:
Acidity Relief Tips:

Quick Fix: Drink warm water with a pinch of baking soda.
Avoid Trigger Foods: Spicy, fried, or acidic foods.
Posture Matters: Stay upright after meals.
Try Natural Remedies: Ginger or aloe vera juice.
Do your symptoms occur frequently? I can suggest lifestyle changes to prevent future issues!
note: dont use "**" and make the response lively and colorful
    """

    mistral_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 600,
        "temperature": 0.7
    }

    try:
        response = requests.post(mistral_url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors

        result = response.json()

    # Safely extracting recommendation from JSON response
        choices = result.get("choices", [])
        if choices and isinstance(choices, list):
            recommendation = choices[0].get("message", {}).get("content", "")
        else:
            recommendation = "No recommendation available."

    # Format recommendation into categories (replacing '$' with '•')
        f_recommendation = recommendation.replace("$", "•").strip()

    # Format for HTML output (optional)
        formatted_html = f_recommendation.replace("\n", "<br>")

        return jsonify({"response": formatted_html})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recommend')
@login_required
def recommend():
    # Get the latest recommendation for the current user
    recommendation = Recommendation.query.filter_by(
        user_id=current_user.id).order_by(Recommendation.created_at.desc()).first()

    if not recommendation:
        flash("Please complete the health questionnaire to get personalized recommendations.", "info")
        return redirect(url_for('questionnaire'))

    recommendation_date = recommendation.created_at.strftime(
        "%B %d, %Y at %I:%M %p")

    return render_template('recommend.html',
                           sleep_recommendation=recommendation.sleep_recommendation,
                           diet_recommendation=recommendation.diet_recommendation,
                           exercise_recommendation=recommendation.exercise_recommendation,
                           weight_management_recommendation=recommendation.weight_management_recommendation,
                           risk_prediction_recommendation=recommendation.risk_prediction_recommendation)

# Handle Form Submission and Generate Recommendations


@app.route("/submit", methods=["POST"])
def handle_submission():
    # Debug: Print all form data to see what's being received
    print("Form data:", request.form)

    # Collect form data with default values for required fields
    form_data = {
        "age": request.form.get("age", "0"),
        "gender": request.form.get("gender", "Not specified"),
        "height": request.form.get("height", "0"),
        "weight": request.form.get("weight", "0"),
        "heart_rate": request.form.get("heart-rate", "0"),
        "sleep": request.form.get("sleep", "0"),
        # Fix the hyphenated field names and provide defaults
        "physical_activity": request.form.get("physical_activity", "Not specified"),
        "water_intake": request.form.get("water_intake", "0"),
        "diet": request.form.getlist("diet"),
        "chronic_conditions": request.form.get("chronic_conditions", "None"),
        "allergies": request.form.get("allergies", "None"),
        "smoking": request.form.get("smoking", "No"),
        "alcohol": request.form.get("alcohol", "No"),
    }

    # Sanitize text inputs
    form_data["gender"] = sanitize_input(form_data["gender"], max_length=20)
    form_data["physical_activity"] = sanitize_input(form_data["physical_activity"], max_length=50)
    form_data["chronic_conditions"] = sanitize_input(form_data["chronic_conditions"], max_length=200)
    form_data["allergies"] = sanitize_input(form_data["allergies"], max_length=200)
    form_data["smoking"] = sanitize_input(form_data["smoking"], max_length=10)
    form_data["alcohol"] = sanitize_input(form_data["alcohol"], max_length=10)

    # Convert string values to appropriate types
    try:
        # Validate numeric inputs
        age = int(form_data["age"])
        height = float(form_data["height"])
        weight = float(form_data["weight"])
        heart_rate = int(form_data["heart_rate"])
        sleep = float(form_data["sleep"])
        water_intake = float(form_data["water_intake"])
        
        # Basic range validation
        if not (1 <= age <= 150):
            raise ValueError("Age must be between 1 and 150")
        if not (50 <= height <= 300):
            raise ValueError("Height must be between 50cm and 300cm")
        if not (10 <= weight <= 500):
            raise ValueError("Weight must be between 10kg and 500kg")
        if not (30 <= heart_rate <= 250):
            raise ValueError("Heart rate must be between 30 and 250 bpm")
        if not (0 <= sleep <= 24):
            raise ValueError("Sleep hours must be between 0 and 24")
        if not (0 <= water_intake <= 20):
            raise ValueError("Water intake must be between 0 and 20 liters")
        
        # Save health record to database
        health_record = HealthRecord(
            user_id=current_user.id,
            age=age,
            gender=form_data["gender"],
            height=float(form_data["height"]),
            weight=float(form_data["weight"]),
            heart_rate=int(form_data["heart_rate"]),
            sleep=float(form_data["sleep"]),
            physical_activity=form_data["physical_activity"],
            water_intake=float(form_data["water_intake"]),
            diet=", ".join(form_data["diet"]) if form_data["diet"] else "None",
            chronic_conditions=form_data["chronic_conditions"],
            allergies=form_data["allergies"],
            smoking=form_data["smoking"],
            alcohol=form_data["alcohol"]
        )
        db.session.add(health_record)
        db.session.commit()

        prompt = f"""
Based on the following user details:
- Age: {form_data['age']}
- Gender: {form_data['gender']}
- Height: {form_data['height']} cm
- Weight: {form_data['weight']} kg
- Heart Rate: {form_data['heart_rate']} bpm
- Sleep: {form_data['sleep']} hours/day
- Physical Activity: {form_data['physical_activity']}
- Water Intake: {form_data['water_intake']} liters/day
- Diet Preferences: {', '.join(form_data['diet']) if form_data['diet'] else 'None'}
- Chronic Conditions: {form_data['chronic_conditions']}
- Allergies: {form_data['allergies']}
- Smoking: {form_data['smoking']}
- Alcohol: {form_data['alcohol']}

Provide unique and accurate personalized health recommendations on the basis of above
information(consider yourslef as health expert)
1) Sleep Hours: advice on sleep duration based on the health data in short in 2-3 bullet
points each on a new line.
2) Diet and Water Intake: diet recommendation with required nutrition based on health data
in short in 2-3 bullet points each on a new line.
3) Exercise/Yoga/Workout: Provide exercise, yoga, or fitness routines in particular that suit
the user's needs in short in 2-3 bullet points on a new line.
4) Weight Management: Guidance on maintaining a healthy weight to loose or gain by
mentioning the exact weight, improving metabolism, and lifestyle changes in
understandable words in short in 2-3 bullet points each on a new line.
5)Risk Prediction:Predict the health risks as high or low and give the habits(same health
data) which are causing it.
small instruction : give the bullet point as $
"""

        mistral_url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {mistral_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-large-latest",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 600,
            "temperature": 0.7
        }

        try:
            response = requests.post(mistral_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            recommendation = result.get("choices")[0].get(
                "message", {}).get("content", "")

            # Format recommendation into categories
            f_recommendation = recommendation.replace("$", "•").strip()

            categories = {
                "sleep": "",
                "diet": "",
                "exercise": "",
                "weight_management": "",
                "risk_prediction": ""
            }

            if f_recommendation:
                lines = f_recommendation.split("\n")
                current_category = None

                for line in lines:
                    line = line.strip()
                    if "Sleep Hours" in line:
                        current_category = "sleep"
                    elif "Diet and Water Intake" in line:
                        current_category = "diet"
                    elif "Exercise/Yoga/Workout" in line:
                        current_category = "exercise"
                    elif "Weight Management" in line:
                        current_category = "weight_management"
                    elif "Risk Prediction" in line:
                        current_category = "risk_prediction"
                    elif current_category:
                        categories[current_category] += line + "<br>"
            if current_user.is_authenticated:
                # Create a new recommendation record
                new_recommendation = Recommendation(
                    user_id=current_user.id,
                    sleep_recommendation=categories["sleep"],
                    diet_recommendation=categories["diet"],
                    exercise_recommendation=categories["exercise"],
                    weight_management_recommendation=categories["weight_management"],
                    risk_prediction_recommendation=categories["risk_prediction"]
                )
                db.session.add(new_recommendation)
                db.session.commit()

                # Redirect to the recommendations page
                return redirect(url_for('recommend'))

            return render_template(
                "recommend.html",
                sleep_recommendation=categories["sleep"],
                diet_recommendation=categories["diet"],
                exercise_recommendation=categories["exercise"],
                weight_management_recommendation=categories["weight_management"],
                risk_prediction_recommendation=categories["risk_prediction"]
            )

        except requests.exceptions.HTTPError as e:
            categories = {
                "sleep": "Error: Unable to generate recommendations.",
                "diet": "Error: Unable to generate recommendations.",
                "exercise": "Error: Unable to generate recommendations.",
                "weight_management": "Error: Unable to generate recommendations.",
                "risk_prediction": "Error:Unable to generate recommendations."
            }

            return render_template(
                "recommend.html",
                sleep_recommendation=categories["sleep"],
                diet_recommendation=categories["diet"],
                exercise_recommendation=categories["exercise"],
                weight_management_recommendation=categories["weight_management"],
                risk_prediction_recommendation=categories["risk_prediction"]
            )
    except Exception as e:
        # Handle any errors during conversion or database operations
        print(f"Error in handle_submission: {str(e)}")
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('questionnaire'))


if __name__ == "__main__":
    app.run(debug=True)
