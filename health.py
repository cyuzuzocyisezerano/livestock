from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



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
