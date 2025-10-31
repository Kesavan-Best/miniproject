from app import app, db, Patient
from datetime import datetime, timedelta
import random

# Sample data for generating realistic patient records
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Alexander", "Rachel", "Patrick", "Catherine", "Frank", "Carolyn", "Dennis", "Janet",
    "Jerry", "Ruth", "Tyler", "Maria", "Aaron", "Heather", "Jose", "Diane"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez"
]

diagnoses = [
    "Hypertension with complications",
    "Type 2 Diabetes Mellitus",
    "Acute Myocardial Infarction",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "Pneumonia",
    "Congestive Heart Failure",
    "Acute Appendicitis",
    "Urinary Tract Infection",
    "Gastroenteritis",
    "Acute Kidney Injury",
    "Sepsis",
    "Stroke (Cerebrovascular Accident)",
    "Asthma Exacerbation",
    "Cholecystitis",
    "Pancreatitis",
    "Deep Vein Thrombosis",
    "Pulmonary Embolism",
    "Cellulitis",
    "Migraine",
    "Atrial Fibrillation",
    "Chronic Kidney Disease",
    "Osteoarthritis",
    "Rheumatoid Arthritis",
    "Anemia",
    "Hypothyroidism",
    "Hyperthyroidism",
    "Liver Cirrhosis",
    "Hepatitis",
    "Diverticulitis",
    "Bowel Obstruction",
    "Peptic Ulcer Disease",
    "Gastroesophageal Reflux Disease (GERD)",
    "Chronic Back Pain",
    "Fracture - Femur",
    "Fracture - Tibia/Fibula",
    "Head Injury",
    "Chest Pain - Cardiac Workup",
    "Syncope",
    "Dehydration",
    "Electrolyte Imbalance"
]

physicians = [
    "Dr. Sarah Wilson", "Dr. Michael Chen", "Dr. Emily Brown", "Dr. James Taylor",
    "Dr. Robert Anderson", "Dr. Lisa Martinez", "Dr. David Thompson", "Dr. Jennifer White",
    "Dr. William Garcia", "Dr. Maria Rodriguez", "Dr. Richard Lee", "Dr. Nancy Harris",
    "Dr. Christopher Moore", "Dr. Karen Jackson", "Dr. Daniel Lewis", "Dr. Susan Clark",
    "Dr. Matthew Robinson", "Dr. Jessica Walker", "Dr. Anthony Hall", "Dr. Laura Allen",
    "Dr. Mark Young", "Dr. Amanda King", "Dr. Donald Wright", "Dr. Michelle Scott",
    "Dr. Steven Hill", "Dr. Melissa Green", "Dr. Paul Adams", "Dr. Kimberly Baker"
]

statuses = ["admitted", "observation", "appointment", "emergency", "discharged"]

medical_notes_templates = [
    "Patient presented to ED with {complaint}. Vital signs stable. {treatment} Initial labs drawn. {plan}",
    "Admitted for {complaint}. Physical examination reveals {findings}. {treatment} Patient responding well to treatment. {plan}",
    "{complaint} noted on admission. Past medical history significant for {history}. {treatment} Close monitoring required. {plan}",
    "Chief complaint: {complaint}. Patient appears {condition}. {treatment} Consulted with specialists. {plan}",
    "Emergency admission for {complaint}. Immediate intervention performed. {treatment} Patient stabilized. {plan}",
]

complaints = [
    "chest pain and shortness of breath",
    "severe abdominal pain",
    "high fever and cough",
    "altered mental status",
    "syncope episode",
    "severe headache",
    "difficulty breathing",
    "acute onset weakness",
    "uncontrolled blood sugar",
    "persistent vomiting",
    "acute joint pain",
    "severe back pain",
    "suspected infection",
    "traumatic injury",
    "seizure activity"
]

findings = [
    "tenderness in affected area",
    "decreased breath sounds bilaterally",
    "irregular heart rhythm",
    "elevated blood pressure",
    "signs of dehydration",
    "limited range of motion",
    "focal neurological deficits",
    "abdominal distension",
    "peripheral edema",
    "altered consciousness"
]

treatments = [
    "Started on IV antibiotics and fluids.",
    "Pain management protocol initiated.",
    "Oxygen therapy commenced.",
    "Cardiac monitoring established.",
    "Emergency surgery scheduled.",
    "Medication regimen adjusted.",
    "Imaging studies ordered and completed.",
    "Specialist consultation obtained.",
    "Physical therapy evaluation pending.",
    "Discharge planning initiated."
]

plans = [
    "Continue current management and reassess in 24 hours.",
    "Schedule follow-up appointment in 2 weeks.",
    "Patient education provided regarding medications.",
    "Transfer to ICU if condition deteriorates.",
    "Awaiting final lab results before discharge.",
    "Family meeting scheduled to discuss care plan.",
    "Recommend outpatient rehabilitation.",
    "Monitor vital signs every 4 hours.",
    "Consult with cardiology for further evaluation.",
    "Discharge home with home health services."
]

histories = [
    "hypertension and diabetes",
    "previous cardiac events",
    "chronic respiratory disease",
    "renal insufficiency",
    "multiple surgeries",
    "autoimmune disorders",
    "psychiatric conditions",
    "substance use history",
    "multiple allergies"
]

conditions = [
    "stable but uncomfortable",
    "in moderate distress",
    "alert and oriented",
    "lethargic but responsive",
    "anxious and restless",
    "comfortable at rest",
    "fatigued but cooperative"
]

def generate_detailed_notes():
    template = random.choice(medical_notes_templates)
    note = template.format(
        complaint=random.choice(complaints),
        findings=random.choice(findings),
        treatment=random.choice(treatments),
        plan=random.choice(plans),
        history=random.choice(histories),
        condition=random.choice(conditions)
    )
    
    # Add additional clinical details
    additional_details = [
        f"\n\nVital Signs: BP {random.randint(100,180)}/{random.randint(60,110)}, HR {random.randint(60,120)}, Temp {random.uniform(97.0,102.0):.1f}°F, RR {random.randint(12,24)}, O2 Sat {random.randint(92,100)}%",
        f"\n\nMedications: {random.choice(['Lisinopril 10mg daily', 'Metformin 500mg BID', 'Aspirin 81mg daily', 'Atorvastatin 20mg daily', 'Levothyroxine 50mcg daily'])}",
        f"\n\nAllergies: {random.choice(['NKDA (No Known Drug Allergies)', 'Penicillin', 'Sulfa drugs', 'Latex', 'Shellfish'])}",
        f"\n\nLab Results: {random.choice(['WBC elevated at 12.5', 'Hemoglobin 11.2 g/dL', 'Creatinine 1.4 mg/dL', 'Glucose 156 mg/dL', 'Troponin negative'])}",
        f"\n\nImaging: {random.choice(['Chest X-ray shows no acute findings', 'CT scan pending', 'Ultrasound completed', 'MRI scheduled for tomorrow', 'EKG shows normal sinus rhythm'])}",
        f"\n\nConsultations: {random.choice(['Cardiology consulted', 'Surgery evaluation completed', 'Nephrology following', 'Infectious disease recommendations obtained', 'Social work involved'])}",
    ]
    
    # Add 2-4 random additional details
    num_details = random.randint(2, 4)
    for _ in range(num_details):
        note += random.choice(additional_details)
    
    return note

def add_bulk_patients(count=90):
    """Add specified number of patient records to the database"""
    
    with app.app_context():
        # Check current patient count
        existing_count = Patient.query.count()
        print(f"Current patient count: {existing_count}")
        
        patients_added = 0
        
        for i in range(count):
            # Generate random dates
            days_ago = random.randint(1, 180)
            admission_date = datetime.now().date() - timedelta(days=days_ago)
            
            # Generate birth date (age between 18 and 90)
            age_years = random.randint(18, 90)
            date_of_birth = datetime.now().date() - timedelta(days=age_years*365 + random.randint(0, 365))
            
            # Generate patient data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            gender = random.choice(["male", "female"])
            
            # Generate unique contact number
            contact_number = f"555-{random.randint(1000, 9999)}"
            
            # Generate email
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com"
            
            # Create patient record
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                contact_number=contact_number,
                email=email,
                primary_diagnosis=random.choice(diagnoses),
                attending_physician=random.choice(physicians),
                admission_date=admission_date,
                status=random.choice(statuses),
                notes=generate_detailed_notes()
            )
            
            try:
                db.session.add(patient)
                patients_added += 1
                
                # Commit in batches of 10
                if patients_added % 10 == 0:
                    db.session.commit()
                    print(f"Added {patients_added} patients...")
            
            except Exception as e:
                print(f"Error adding patient {i+1}: {str(e)}")
                db.session.rollback()
                continue
        
        # Final commit for remaining patients
        try:
            db.session.commit()
            print(f"\n✓ Successfully added {patients_added} new patient records!")
            print(f"Total patients in database: {Patient.query.count()}")
        except Exception as e:
            print(f"Error in final commit: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("Adding 90 new patient records to the database...")
    print("This will bring the total to approximately 90-100 patients including existing records.\n")
    
    add_bulk_patients(90)
    
    print("\n✓ Bulk patient import completed!")
