from flask import Flask, render_template_string, request
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login.html'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already in use.')
            return redirect(url_for('register'))
        
        # Create new user with hashed password
        new_user = User(username=username, 
                        email=email, 
                        password_hash=generate_password_hash(password))
        
        # Add user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('templates', filename='login'))
    
    return render_template('login-registration-system.py')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            flash('Logged in successfully!')
            return redirect(url_for('templates', filename='index.html'))
        else:
            flash('Invalid username or password.')
    
    return render_template('app.py')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('templates', filename='login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

# Database of diseases and remedies
disease_database = {
    'cattle': [
        {
            'id': 1,
            'name': "Bovine Respiratory Disease (BRD)",
            'symptoms': ["coughing", "nasal discharge", "fever", "reduced appetite", "labored breathing"],
            'description': "A complex of diseases affecting the lungs and respiratory tract of cattle.",
            'severity': "High",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Antibiotics like florfenicol, tulathromycin, or tilmicosin as prescribed by a veterinarian."
                },
                {
                    'type': "Management",
                    'details': "Provide good ventilation, reduce stress, isolate affected animals."
                },
                {
                    'type': "Prevention",
                    'details': "Vaccination against viral pathogens, proper nutrition, and stress management."
                }
            ]
        },
        {
            'id': 2,
            'name': "Foot and Mouth Disease",
            'symptoms': ["fever", "blisters on mouth", "blisters on feet", "excessive salivation", "lameness"],
            'description': "A highly contagious viral disease affecting cloven-hoofed animals.",
            'severity': "Critical - Reportable Disease",
            'treatments': [
                {
                    'type': "Action Required",
                    'details': "Contact veterinary authorities immediately. This is a notifiable disease."
                },
                {
                    'type': "Management",
                    'details': "Quarantine affected animals, implement biosecurity measures."
                },
                {
                    'type': "Treatment",
                    'details': "Supportive care only. Treatment focuses on pain management and preventing secondary infections."
                }
            ]
        },
        {
            'id': 3,
            'name': "Mastitis",
            'symptoms': ["swollen udder", "abnormal milk", "pain in udder", "reduced milk production", "fever"],
            'description': "Inflammation of the mammary gland usually caused by bacterial infection.",
            'severity': "Moderate to High",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Intramammary antibiotics, systemic antibiotics for severe cases as prescribed by vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Frequent milking, cold or warm compresses, anti-inflammatory drugs."
                },
                {
                    'type': "Prevention",
                    'details': "Good milking hygiene, proper housing, teat dipping after milking."
                }
            ]
        }
    ],
    'goat': [
        {
            'id': 1,
            'name': "Caprine Arthritis Encephalitis (CAE)",
            'symptoms': ["joint swelling", "lameness", "weight loss", "pneumonia", "neurological symptoms"],
            'description': "A viral disease affecting goats that causes chronic progressive arthritis and encephalitis.",
            'severity': "High - No Cure",
            'treatments': [
                {
                    'type': "Management",
                    'details': "No specific treatment. Manage pain with anti-inflammatory drugs prescribed by a vet."
                },
                {
                    'type': "Prevention",
                    'details': "Testing and culling, separating kids from infected dams at birth."
                },
                {
                    'type': "Supportive Care",
                    'details': "Provide comfortable bedding, easy access to food and water."
                }
            ]
        },
        {
            'id': 2,
            'name': "Enterotoxemia (Overeating Disease)",
            'symptoms': ["sudden death", "abdominal pain", "diarrhea", "convulsions", "bloating"],
            'description': "Caused by Clostridium perfringens bacteria that produce toxins in the intestine.",
            'severity': "Critical",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Antitoxin, antibiotics, anti-inflammatories as prescribed by vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Oral electrolytes, IV fluids, reduce feed intake temporarily."
                },
                {
                    'type': "Prevention",
                    'details': "Vaccination, gradual diet changes, avoid overfeeding grain."
                }
            ]
        },
        {
            'id': 3,
            'name': "Coccidiosis",
            'symptoms': ["diarrhea", "weight loss", "dehydration", "weakness", "bloody stool"],
            'description': "A parasitic disease caused by protozoa affecting the intestinal tract.",
            'severity': "Moderate",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Sulfa drugs, amprolium, or other coccidiostats as prescribed by a vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Fluids to prevent dehydration, electrolytes, good nutrition."
                },
                {
                    'type': "Prevention",
                    'details': "Clean housing, prevent overcrowding, good sanitation, coccidiostats in feed for prevention."
                }
            ]
        }
    ]
}

# Common symptoms for each animal type
symptoms = {
    'cattle': [
        "coughing", "nasal discharge", "fever", "reduced appetite", "labored breathing", 
        "swollen udder", "abnormal milk", "pain in udder", "reduced milk production",
        "blisters on mouth", "blisters on feet", "excessive salivation", "lameness",
        "diarrhea", "weight loss", "dehydration", "weakness", "bloody stool"
    ],
    'goat': [
        "joint swelling", "lameness", "weight loss", "pneumonia", "neurological symptoms",
        "sudden death", "abdominal pain", "diarrhea", "convulsions", "bloating",
        "dehydration", "weakness", "bloody stool", "fever", "coughing", "reduced appetite"
    ]
}

# Rule-based disease diagnostic system
class LivestockHealthAdvisor:
    def __init__(self):
        self.disease_database = disease_database
        self.symptoms = symptoms
        
    # Rule 1: Filter diseases based on selected symptoms
    def filter_by_symptoms(self, animal_type, selected_symptoms):
        if not selected_symptoms:
            return self.disease_database[animal_type]
            
        filtered_diseases = []
        for disease in self.disease_database[animal_type]:
            # Check if any selected symptom matches the disease
            if any(symptom in disease['symptoms'] for symptom in selected_symptoms):
                filtered_diseases.append(disease)
        
        return filtered_diseases
    
    # Rule 2: Sort diseases by symptom match count (highest first)
    def sort_by_match_count(self, diseases, selected_symptoms):
        if not selected_symptoms:
            return diseases
            
        # Count matching symptoms for each disease and sort
        return sorted(
            diseases,
            key=lambda disease: sum(1 for s in selected_symptoms if s in disease['symptoms']),
            reverse=True
        )
    
    # Rule 3: Filter by search text in name, description, or symptoms
    def filter_by_search_text(self, diseases, search_text):
        if not search_text:
            return diseases
            
        filtered_diseases = []
        search_text = search_text.lower()
        
        for disease in diseases:
            # Check if text is in disease name
            if search_text in disease['name'].lower():
                filtered_diseases.append(disease)
                continue
                
            # Check if text is in description
            if search_text in disease['description'].lower():
                filtered_diseases.append(disease)
                continue
                
            # Check if text is in any symptom
            if any(search_text in symptom for symptom in disease['symptoms']):
                filtered_diseases.append(disease)
                continue
                
        return filtered_diseases
    
    # Rule 4: Identify critical conditions that require immediate veterinary attention
    def flag_critical_conditions(self, diseases):
        for disease in diseases:
            if "Critical" in disease['severity']:
                disease['urgent'] = True
            else:
                disease['urgent'] = False
        return diseases
    
    # Rule 5: Calculate symptom coverage percentage
    def calculate_symptom_coverage(self, diseases, selected_symptoms):
        if not selected_symptoms:
            for disease in diseases:
                disease['symptom_coverage'] = 0
            return diseases
            
        for disease in diseases:
            matching_symptoms = [s for s in selected_symptoms if s in disease['symptoms']]
            disease['matching_symptoms'] = matching_symptoms
            disease['symptom_coverage'] = len(matching_symptoms) / len(selected_symptoms) * 100
            
        return diseases
    
    # Rule 6: Apply severity rating score
    def apply_severity_rating(self, diseases):
        severity_score = {
            "Low": 1,
            "Moderate": 2,
            "Moderate to High": 3,
            "High": 4,
            "Critical": 5,
            "Critical - Reportable Disease": 5
        }
        
        for disease in diseases:
            # Extract base severity without additional text
            base_severity = disease['severity'].split(' - ')[0] if ' - ' in disease['severity'] else disease['severity']
            disease['severity_score'] = severity_score.get(base_severity, 0)
            
        return diseases
    
    # Main search method that applies all rules
    def search_diseases(self, animal_type, selected_symptoms, search_text):
        # Apply rules in sequence
        results = self.filter_by_symptoms(animal_type, selected_symptoms)
        results = self.sort_by_match_count(results, selected_symptoms)
        results = self.filter_by_search_text(results, search_text)
        results = self.flag_critical_conditions(results)
        results = self.calculate_symptom_coverage(results, selected_symptoms)
        results = self.apply_severity_rating(results)
        
        return results

# Initialize our health advisor
health_advisor = LivestockHealthAdvisor()

# HTML Templates as strings

# Index template
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Livestock Health Advisor</title>
    <style>
        :root {
            --gold: #D4AF37;
            --black: #1a1a1a;
            --light-gold: #F5E6B4;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        
        body {
            background-color: var(--black);
            color: var(--gold);
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid var(--gold);
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: var(--light-gold);
            margin-bottom: 20px;
        }
        .animal-selector {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .animal-type {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            padding: 10px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .animal-type img {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 50%;
            margin-bottom: 10px;
            border: 2px solid var(--gold);
        }
        .active {
            border-color: #007bff;
            background-color: #f0f7ff;
        }
        .search-section {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--gold);
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .search-box input {
            flex-grow: 1;
            padding: 10px;
            font-size: 1em;
        }
        .search-box button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        .symptoms-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .symptom-checkbox {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .emergency-banner {
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .disease-card {
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 4px solid var(--gold);
        }
        .disease-name {
            font-size: 1.5rem;
            color: var(--gold);
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .severity {
            font-size: 0.9rem;
            padding: 4px 8px;
            border-radius: 4px;
            background-color: var(--gold);
            color: var(--black);
        }
        .disease-details {
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }
        .disease-image {
            flex: 0 0 150px;
            margin-right: 15px;
            width: 200px;
            height: 150px;
            background-color: #333;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--gold);
        }
        .disease-image img {
             width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .disease-info {
            flex-grow: 1;
        }
        .treatment-section {
             margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(212, 175, 55, 0.3);
        }
        .treatment-option {
            margin-bottom: 15px;
        }
        .treatment-option h4 {
            color: var(--light-gold);
            margin-bottom: 5px;
        }
        .emergency-banner {
            background-color: rgba(255, 0, 0, 0.2);
            color: #ff9999;
            text-align: center;
            padding: 15px;
            border-radius: 8px;

            margin: 20px 0;
            border: 1px solid #ff6666;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px 0;
            border-top: 1px solid var(--gold);
            color: var(--light-gold);
        }
    </style>
</head>
<body>
<div class="container">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="message">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>

<!-- register.html -->
{% extends "base.html" %}
{% block content %}
<h1>Register</h1>
<form method="POST" action="{{ url_for('register') }}">
    <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
    </div>
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
    </div>
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
    </div>
    <div class="form-group">
        <button type="submit">Register</button>
    </div>
    <div class="links">
        Already have an account? <a href="{{ url_for('login') }}">Login</a>
    </div>
</form>
{% endblock %}

<!-- login.html -->
{% extends "base.html" %}
{% block content %}
<h1>Login</h1>
<form method="POST" action="{{ url_for('login') }}">
    <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
    </div>
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
    </div>
    <div class="form-group">
        <button type="submit">Login</button>
    </div>
    <div class="links">
        Don't have an account? <a href="{{ url_for('register') }}">Register</a>
    </div>
</form>
{% endblock %}

<!-- home.html -->
{% extends "base.html" %}
{% block content %}
<h1>Welcome, {{ username }}!</h1>
<p>You have successfully logged in.</p>
<div class="form-group">
    <a href="{{ url_for('logout') }}"><button>Logout</button></a>
</div>
{% endblock %}

    <div class="container">
        <header>
            <h1>Livestock Health Advisor</h1>
            <div class="subtitle">Expert Remedies for Goats & Cattle</div>
        </header>
        
        <div class="main-content">
            <form action="/search" method="post" class="search-section">
                <div class="animal-selector">
                    <div class="animal-type {% if animal_type == 'cattle' or not animal_type %}active{% endif %}" id="cattle-selector">
                        <img src="/static/images/cows-3614642_1280.jpg" alt="Cattle">
                        <span>Cattle</span>
                        <input type="radio" name="animal_type" value="cattle" {% if animal_type == 'cattle' or not animal_type %}checked{% endif %} style="display: none;">
                    </div>
                    <div class="animal-type {% if animal_type == 'goat' %}active{% endif %}" id="goat-selector">
                        <img src="/static/images/irish-goat-7429437_1280.jpg" alt="Goat">
                        <span>Goat</span>
                        <input type="radio" name="animal_type" value="goat" {% if animal_type == 'goat' %}checked{% endif %} style="display: none;">
                    </div>
                </div>
                
                <div class="search-box">
                    <input type="text" id="search-input" name="search_text" placeholder="Search symptoms or diseases...">
                    <button type="submit">Find Remedies</button>
                </div>
                
                <div>
                    <h3>Select Symptoms:</h3>
                    <div class="symptoms-container" id="cattle-symptoms" {% if animal_type == 'goat' %}style="display: none;"{% endif %}>
                        {% for symptom in cattle_symptoms %}
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="cattle-{{ symptom }}" name="symptoms" value="{{ symptom }}">
                            <label for="cattle-{{ symptom }}">{{ symptom[0]|upper }}{{ symptom[1:] }}</label>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <div class="symptoms-container" id="goat-symptoms" {% if animal_type != 'goat' %}style="display: none;"{% endif %}>
                        {% for symptom in goat_symptoms %}
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="goat-{{ symptom }}" name="symptoms" value="{{ symptom }}">
                            <label for="goat-{{ symptom }}">{{ symptom[0]|upper }}{{ symptom[1:] }}</label>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </form>
            
            <div class="emergency-banner">
                <strong>Important:</strong> In case of severe symptoms or emergency, contact a veterinarian immediately.
            </div>
        </div>
        
        <footer>
            <p>This tool provides general information only. Always consult with a qualified veterinarian for diagnosis and treatment.</p>
            <p>&copy; 2025 Livestock Health Advisor</p>
        </footer>
    </div>
    
    <script>
        // Simple JavaScript to toggle between animal types
        document.getElementById('cattle-selector').addEventListener('click', function() {
            document.querySelector('input[value="cattle"]').checked = true;
            document.getElementById('cattle-selector').classList.add('active');
            document.getElementById('goat-selector').classList.remove('active');
            document.getElementById('cattle-symptoms').style.display = 'grid';
            document.getElementById('goat-symptoms').style.display = 'none';
        });
        
        document.getElementById('goat-selector').addEventListener('click', function() {
            document.querySelector('input[value="goat"]').checked = true;
            document.getElementById('goat-selector').classList.add('active');
            document.getElementById('cattle-selector').classList.remove('active');
            document.getElementById('goat-symptoms').style.display = 'grid';
            document.getElementById('cattle-symptoms').style.display = 'none';
        });
    </script>
</body>
</html>
'''

# Results
RESULTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Livestock Health Advisor - Results</title>
    <style>
       :root {
            --gold: #D4AF37;
            --black: #1a1a1a;
            --light-gold: #F5E6B4;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        
        body {
            background-color: var(--black);
            color: var(--gold);
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 1.2em;
            color: #666;
        }
        .emergency-banner {
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .result-section {
            margin-bottom: 30px;
        }
        .disease-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .disease-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .severity {
            background-color: #f8d7da;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .critical {
            background-color: #dc3545;
            color: white;
        }
        .high {
            background-color: #f8d7da;
        }
        .moderate {
            background-color: #fff3cd;
        }
        .low {
            background-color: #d1e7dd;
        }
        .disease-details {
            display: flex;
            margin-top: 15px;
        }
        .disease-image {
            flex: 0 0 150px;
            margin-right: 15px;
        }
        .disease-image img {
            max-width: 100%;
            height: auto;
        }
        .disease-info {
            flex-grow: 1;
        }
        .treatment-section {
            margin-top: 10px;
        }
        .treatment-option {
            margin-bottom: 10px;
        }
        .back-button {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background-color: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .symptom-coverage {
            margin-top: 10px;
            font-style: italic;
        }
        .matching-symptoms {
            background-color: #e2f0d9;
            padding: 5px;
            border-radius: 3px;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Livestock Health Advisor</h1>
            <div class="subtitle">Expert Remedies for Goats & Cattle</div>
        </header>
        
        <a href="/" class="back-button">« Back to Search</a>
        
        <div class="main-content">
            <div class="emergency-banner">
                <strong>Important:</strong> In case of severe symptoms or emergency, contact a veterinarian immediately.
            </div>
            
            <div class="result-section">
                <h2>Possible Conditions for {{ animal_type|capitalize }}:</h2>
                
                {% if selected_symptoms %}
                <p>
                    <strong>Selected symptoms:</strong> 
                    {% for symptom in selected_symptoms %}
                        <span class="matching-symptoms">{{ symptom[0]|upper }}{{ symptom[1:] }}</span>{% if not loop.last %}, {% endif %}
                    {% endfor %}
                </p>
                {% endif %}
                
                <div id="disease-results">
                    {% if results|length == 0 %}
                        <p>No matching conditions found. Try selecting different symptoms or consult a veterinarian.</p>
                    {% else %}
                        {% for disease in results %}
                            <div class="disease-card">
                                <div class="disease-name">
                                    {{ disease.name }} 
                                    <span class="severity {% if disease.severity_score >= 5 %}critical{% elif disease.severity_score >= 4 %}high{% elif disease.severity_score >= 2 %}moderate{% else %}low{% endif %}">
                                        {{ disease.severity }}
                                    </span>
                                    {% if disease.urgent %}
                                        <span style="color: red; font-weight: bold; margin-left: 10px;">URGENT: CONTACT VET IMMEDIATELY</span>
                                    {% endif %}
                                </div>
                                
                                <p>{{ disease.description }}</p>
                                
                                <p><strong>Symptoms:</strong> 
                                    {% for symptom in disease.symptoms %}
                                        {% if selected_symptoms and symptom in selected_symptoms %}
                                            <span class="matching-symptoms">{{ symptom[0]|upper }}{{ symptom[1:] }}</span>
                                        {% else %}
                                            {{ symptom[0]|upper }}{{ symptom[1:] }}
                                        {% endif %}
                                        {% if not loop.last %}, {% endif %}
                                    {% endfor %}
                                </p>
                                
                                {% if selected_symptoms and disease.matching_symptoms %}
                                    <p class="symptom-coverage">
                                        <strong>Symptom match:</strong> {{ disease.symptom_coverage|round(1) }}% ({{ disease.matching_symptoms|length }} of {{ selected_symptoms|length }} symptoms)
                                    </p>
                                {% endif %}
                                
                                <div class="disease-details">
                                    <div class="disease-image">
                                        <img src="/static/images/lame goat.jpg" alt="{{ disease.name }}">
                                    </div>
                                    <div class="disease-info">
                                        <div class="treatment-section">
                                            <h3>Recommended Treatments:</h3>
                                            {% for treatment in disease.treatments %}
                                                <div class="treatment-option">
                                                    <h4>{{ treatment.type }}</h4>
                                                    <p>{{ treatment.details }}</p>
                                                </div>
                                            {% endfor %}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>
        
        <footer>
            <p>This tool provides general information only. Always consult with a qualified veterinarian for diagnosis and treatment.</p>
            <p>&copy; 2025 Livestock Health Advisor</p>
        </footer>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        INDEX_TEMPLATE, 
        cattle_symptoms=symptoms['cattle'], 
        goat_symptoms=symptoms['goat'],
        animal_type='cattle'
    )

@app.route('/search', methods=['POST'])
def search():
    # Get data from the form
    animal_type = request.form.get('animal_type', 'cattle')
    search_text = request.form.get('search_text', '')
    selected_symptoms = request.form.getlist('symptoms')
    
    # Apply our rule-based system
    results = health_advisor.search_diseases(animal_type, selected_symptoms, search_text)
    
    return render_template_string(
        RESULTS_TEMPLATE, 
        results=results, 
        animal_type=animal_type, 
        selected_symptoms=selected_symptoms
    )

# For serving static files in development (would need proper setup for production)
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    from flask import send_from_directory
    import os
    # This is only for demo purposes - you'd need to set up proper static file serving for production
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

if __name__ == '__main__':
    import os
    # Create static/images directory if it doesn't exist
    if not os.path.exists(os.path.join(app.root_path, 'static', 'images')):
        os.makedirs(os.path.join(app.root_path, 'static', 'images'))
    
    app.run(debug=True)