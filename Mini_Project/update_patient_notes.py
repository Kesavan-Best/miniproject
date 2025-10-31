#!/usr/bin/env python3
"""Update all patient records with very long detailed medical notes (90-1000 lines)"""

from app import app, db, Patient
from datetime import datetime, timedelta
import random

# Extended medical templates for generating very long notes
chief_complaints = [
    "severe chest pain radiating to left arm",
    "persistent high-grade fever with chills and rigors",
    "acute onset severe headache with photophobia",
    "progressive shortness of breath over 3 days",
    "sudden onset severe abdominal pain in right upper quadrant",
    "altered mental status with confusion and disorientation",
    "severe lower back pain with radiation to legs",
    "recurrent episodes of palpitations and dizziness",
    "unexplained weight loss of 15 kg over 2 months",
    "chronic productive cough with hemoptysis",
]

medical_history = [
    "Patient has a 10-year history of Type 2 Diabetes Mellitus, managed with Metformin 1000mg twice daily and Insulin Glargine 20 units at bedtime.",
    "Long-standing hypertension diagnosed 15 years ago, currently on Amlodipine 10mg and Losartan 50mg with good control.",
    "Previous myocardial infarction 5 years ago, underwent PCI with stent placement in LAD, on dual antiplatelet therapy.",
    "Chronic kidney disease stage 3, with baseline creatinine of 1.8 mg/dL, regular nephrology follow-up.",
    "History of COPD, GOLD stage 2, on Tiotropium inhaler and PRN Salbutamol, ex-smoker with 30 pack-year history.",
    "Previous stroke 3 years ago with residual right-sided weakness, currently on warfarin with regular INR monitoring.",
    "Diagnosed with rheumatoid arthritis 8 years ago, on Methotrexate 15mg weekly and Hydroxychloroquine 400mg daily.",
    "Chronic liver disease secondary to hepatitis C, completed antiviral therapy 2 years ago with sustained virological response.",
]

physical_examination = [
    "General: Patient alert and oriented, appears in moderate distress, lying comfortably in bed.",
    "Vital Signs: BP 145/92 mmHg, HR 98 bpm regular, Temp 38.5°C, RR 22/min, SpO2 94% on room air.",
    "HEENT: Normocephalic, atraumatic, pupils equal and reactive, no scleral icterus, oral mucosa moist.",
    "Cardiovascular: S1 S2 present, regular rhythm, Grade 2/6 systolic murmur at apex, no rubs or gallops.",
    "Respiratory: Bilateral air entry present, scattered rhonchi heard, no wheezes, decreased breath sounds at bases.",
    "Abdomen: Soft, tender in right upper quadrant, Murphy's sign positive, no rebound tenderness, bowel sounds present.",
    "Neurological: Cranial nerves II-XII intact, motor strength 5/5 in all extremities, reflexes 2+ symmetric, no focal deficits.",
    "Extremities: No cyanosis, clubbing present, 2+ pitting edema bilateral lower limbs up to knees.",
]

investigations = [
    "Complete Blood Count: WBC 15,200/μL with 85% neutrophils, Hemoglobin 10.2 g/dL, Platelets 185,000/μL, ESR 45 mm/hr, CRP 12.5 mg/L.",
    "Renal Function: Creatinine 2.1 mg/dL (increased from baseline 1.5), BUN 42 mg/dL, eGFR 35 mL/min/1.73m², Potassium 5.2 mEq/L.",
    "Liver Function: Bilirubin 2.5 mg/dL (1.8 direct), AST 125 U/L, ALT 145 U/L, ALP 280 U/L, Albumin 2.8 g/dL, PT/INR 1.8.",
    "Cardiac Enzymes: Troponin I 2.5 ng/mL (elevated), CK-MB 45 U/L, BNP 850 pg/mL indicating cardiac strain.",
    "Arterial Blood Gas: pH 7.32, PaCO2 52 mmHg, PaO2 68 mmHg, HCO3 24 mEq/L, indicating respiratory acidosis.",
    "Chest X-ray: Bilateral patchy infiltrates in lower zones, cardiomegaly with CTR 0.6, blunting of costophrenic angles suggesting pleural effusion.",
    "ECG: Sinus tachycardia at 110 bpm, ST depression in leads V4-V6, T wave inversions in lateral leads, prolonged QTc 485 ms.",
    "CT Scan: Large heterogeneous mass in right lobe of liver measuring 8.5 x 7.2 cm with central necrosis and peripheral enhancement.",
    "Echocardiography: LV ejection fraction 35%, global hypokinesia, moderate mitral regurgitation, dilated left atrium.",
    "Ultrasound Abdomen: Distended gallbladder with multiple calculi, wall thickening 5mm, positive sonographic Murphy's sign, pericholecystic fluid.",
]

medications = [
    "Aspirin 75mg once daily for cardioprotection",
    "Atorvastatin 80mg at bedtime for lipid management",
    "Metoprolol 50mg twice daily for heart rate control",
    "Furosemide 40mg twice daily for fluid management",
    "Potassium Chloride 20mEq daily for supplementation",
    "Insulin Regular 8 units before meals as per sliding scale",
    "Pantoprazole 40mg before breakfast for gastroprotection",
    "Clopidogrel 75mg once daily as antiplatelet",
    "Warfarin 5mg daily with INR monitoring",
    "Levothyroxine 100mcg once daily for hypothyroidism",
]

treatment_plan = [
    "Admit to telemetry unit for continuous cardiac monitoring and observation of arrhythmias or further cardiac events.",
    "Initiate IV antibiotics - Ceftriaxone 2g daily and Azithromycin 500mg daily for 7-10 days for suspected community-acquired pneumonia.",
    "Start IV fluids - Normal Saline at 100 mL/hour to maintain adequate hydration and support renal perfusion.",
    "Pain management with IV Morphine 2-4mg every 4 hours as needed, monitor respiratory rate and level of consciousness.",
    "Consult cardiology for evaluation and management of acute coronary syndrome, possible cardiac catheterization.",
    "Consult pulmonology for consideration of bronchoscopy and further evaluation of lung pathology.",
    "Consult general surgery for evaluation of acute cholecystitis and possible cholecystectomy.",
    "Order repeat troponins every 6 hours to trend cardiac enzyme levels and assess for ongoing myocardial injury.",
    "Chest physiotherapy twice daily to improve lung expansion and prevent atelectasis.",
    "Maintain strict input-output monitoring, aim for urine output >0.5 mL/kg/hour.",
]

progress_notes = [
    "Day 1: Patient admitted through emergency department. Initial workup completed. Stable hemodynamics. Started on treatment protocol.",
    "Day 2: Patient showing improvement in symptoms. Fever subsided to 37.8°C. Pain score reduced from 8/10 to 5/10. Tolerating oral feeds.",
    "Day 3: Repeat labs show improvement in inflammatory markers. WBC count decreased to 11,200/μL. Patient mobilizing with assistance.",
    "Day 4: Patient developed new onset tachycardia. ECG shows atrial fibrillation. Cardiology consulted. Started on rate control medications.",
    "Day 5: Patient hemodynamically stable. Switched from IV to oral antibiotics. Physical therapy initiated. Family counseling provided.",
    "Day 6: Imaging repeated showing partial resolution of infiltrates. Patient ambulating independently. Discharge planning started.",
    "Day 7: Patient ready for discharge. All medications reconciled. Follow-up appointments scheduled. Patient educated about warning signs.",
]

nursing_notes = [
    "0800hrs: Patient awake, alert, oriented x3. Vital signs stable. No complaints of pain. IV site clean and dry.",
    "1200hrs: Administered medications as ordered. Patient tolerated oral feeds well. No nausea or vomiting reported.",
    "1600hrs: Patient ambulated in hallway with assistance. No signs of distress. SpO2 maintained at 96% on 2L oxygen.",
    "2000hrs: Evening medications given. Patient's daughter visited. Patient in good spirits, watching television.",
    "0000hrs: Patient sleeping comfortably. Vital signs checked, all within normal limits. No events overnight.",
]

specialist_consultations = [
    "CARDIOLOGY CONSULTATION: Reviewed ECG and cardiac markers. Findings consistent with NSTEMI. Recommend cardiac catheterization within 48 hours. Continue dual antiplatelet therapy and statin. Monitor for arrhythmias.",
    "PULMONOLOGY CONSULTATION: Clinical and radiological findings suggestive of hospital-acquired pneumonia. Recommend bronchoscopy for culture and sensitivity. Consider changing antibiotic regimen based on culture results.",
    "NEPHROLOGY CONSULTATION: Acute kidney injury likely prerenal etiology secondary to dehydration. Recommend adequate fluid resuscitation. Avoid nephrotoxic agents. Monitor creatinine and electrolytes daily.",
    "ENDOCRINOLOGY CONSULTATION: Diabetes poorly controlled with HbA1c 9.2%. Recommend adjusting insulin regimen. Consider adding GLP-1 agonist. Patient education regarding diet and lifestyle modifications essential.",
    "INFECTIOUS DISEASE CONSULTATION: Blood cultures grew Streptococcus pneumoniae sensitive to Penicillin. Recommend de-escalating to Penicillin G 2 million units IV every 4 hours. Continue for total 14 days.",
]

def generate_comprehensive_medical_notes():
    """Generate very long comprehensive medical notes (90-1000 lines)"""
    notes = []
    
    # Title
    notes.append("=" * 80)
    notes.append("COMPREHENSIVE MEDICAL RECORD - DETAILED PROGRESS NOTES")
    notes.append("=" * 80)
    notes.append("")
    
    # Chief Complaint
    notes.append("CHIEF COMPLAINT:")
    notes.append("-" * 80)
    notes.append(f"Patient presents with {random.choice(chief_complaints)}.")
    notes.append(f"Symptoms started {random.randint(1, 14)} days ago and have been progressively worsening.")
    notes.append(f"Associated symptoms include {random.choice(['nausea', 'vomiting', 'dizziness', 'weakness', 'fatigue', 'loss of appetite'])}.")
    notes.append("")
    
    # History of Present Illness (HPI) - VERY DETAILED
    notes.append("HISTORY OF PRESENT ILLNESS:")
    notes.append("-" * 80)
    for i in range(random.randint(15, 25)):
        notes.append(f"The patient reports that {random.choice(['initially', 'at first', 'when symptoms began', 'during the early phase'])}, "
                    f"{random.choice(['the discomfort was mild', 'symptoms were tolerable', 'pain was intermittent', 'episodes were brief'])}. "
                    f"However, over the {random.choice(['past few days', 'last week', 'recent days', 'course of time'])}, "
                    f"{random.choice(['symptoms have intensified', 'condition has worsened', 'pain has become severe', 'episodes are more frequent'])}.")
    notes.append("")
    
    # Past Medical History - EXTENSIVE
    notes.append("PAST MEDICAL HISTORY:")
    notes.append("-" * 80)
    for history in random.sample(medical_history, random.randint(4, 7)):
        notes.append(f"• {history}")
        notes.append(f"  - Patient reports good compliance with prescribed medications.")
        notes.append(f"  - Regular follow-up maintained with primary care physician.")
        notes.append("")
    
    # Surgical History
    notes.append("SURGICAL HISTORY:")
    notes.append("-" * 80)
    surgeries = [
        "Appendectomy performed 15 years ago at local hospital, uneventful recovery",
        "Cholecystectomy (laparoscopic) done 8 years ago for symptomatic gallstones",
        "Hernia repair (inguinal) performed 5 years ago, mesh placement done",
        "Knee arthroscopy for meniscal tear 3 years ago, successful outcome"
    ]
    for surgery in random.sample(surgeries, random.randint(1, 3)):
        notes.append(f"• {surgery}")
    notes.append("")
    
    # Medications - DETAILED LIST
    notes.append("CURRENT MEDICATIONS:")
    notes.append("-" * 80)
    for i, med in enumerate(random.sample(medications, random.randint(6, 10)), 1):
        notes.append(f"{i}. {med}")
        notes.append(f"   Last dose: {random.choice(['This morning', 'Last night', 'Yesterday evening', 'Today at noon'])}")
        notes.append(f"   Compliance: {random.choice(['Good', 'Excellent', 'Fair'])}")
    notes.append("")
    
    # Allergies
    notes.append("ALLERGIES:")
    notes.append("-" * 80)
    allergies = ["Penicillin (causes rash)", "Sulfa drugs (causes hives)", "NKDA (No Known Drug Allergies)", 
                 "Latex (contact dermatitis)", "Shellfish (anaphylaxis history)"]
    notes.append(f"• {random.choice(allergies)}")
    notes.append("")
    
    # Social History - DETAILED
    notes.append("SOCIAL HISTORY:")
    notes.append("-" * 80)
    notes.append(f"Occupation: {random.choice(['Teacher', 'Engineer', 'Retired', 'Business owner', 'Healthcare worker', 'Office administrator'])}")
    notes.append(f"Living situation: {random.choice(['Lives with spouse', 'Lives alone', 'Lives with family', 'Lives with children'])}")
    notes.append(f"Smoking: {random.choice(['Never smoker', 'Ex-smoker quit 10 years ago', 'Current smoker 1 pack/day for 20 years', 'Quit 5 years ago'])}")
    notes.append(f"Alcohol: {random.choice(['Social drinker', 'Non-drinker', 'Occasional wine with dinner', 'Denies alcohol use'])}")
    notes.append(f"Exercise: {random.choice(['Sedentary lifestyle', 'Walks 30 minutes daily', 'Moderate activity 3x/week', 'Limited due to medical conditions'])}")
    notes.append(f"Diet: {random.choice(['Regular diet', 'Diabetic diet', 'Low sodium diet', 'Heart healthy diet'])}")
    notes.append("")
    
    # Family History
    notes.append("FAMILY HISTORY:")
    notes.append("-" * 80)
    notes.append(f"• Father: {random.choice(['Died at age 65 from MI', 'Alive with hypertension', 'History of diabetes', 'No significant medical history'])}")
    notes.append(f"• Mother: {random.choice(['Alive with diabetes and hypertension', 'Died from stroke at age 70', 'History of breast cancer', 'Healthy'])}")
    notes.append(f"• Siblings: {random.choice(['1 brother with CAD', '2 sisters, healthy', 'No siblings', 'Sister with diabetes'])}")
    notes.append("")
    
    # Review of Systems - COMPREHENSIVE
    notes.append("REVIEW OF SYSTEMS:")
    notes.append("-" * 80)
    systems = {
        "Constitutional": ["Fever", "Chills", "Night sweats", "Weight loss", "Fatigue"],
        "HEENT": ["Headache", "Vision changes", "Hearing loss", "Sore throat", "Nasal congestion"],
        "Cardiovascular": ["Chest pain", "Palpitations", "Orthopnea", "Leg swelling", "Syncope"],
        "Respiratory": ["Shortness of breath", "Cough", "Wheezing", "Hemoptysis", "Chest tightness"],
        "Gastrointestinal": ["Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal pain"],
        "Genitourinary": ["Dysuria", "Frequency", "Urgency", "Hematuria", "Incontinence"],
        "Musculoskeletal": ["Joint pain", "Muscle weakness", "Back pain", "Limited mobility", "Stiffness"],
        "Neurological": ["Dizziness", "Numbness", "Tingling", "Weakness", "Memory problems"],
        "Psychiatric": ["Depression", "Anxiety", "Sleep disturbance", "Mood changes", "Stress"],
        "Endocrine": ["Heat/cold intolerance", "Excessive thirst", "Polyuria", "Hair loss", "Tremors"]
    }
    
    for system, symptoms in systems.items():
        notes.append(f"{system}:")
        present = random.sample(symptoms, random.randint(1, 3))
        for symptom in present:
            notes.append(f"  • {symptom}: Present, {random.choice(['mild', 'moderate', 'severe'])}")
        notes.append(f"  • All other {system.lower()} symptoms negative")
        notes.append("")
    
    # Physical Examination - VERY DETAILED
    notes.append("PHYSICAL EXAMINATION:")
    notes.append("=" * 80)
    for exam in physical_examination:
        notes.append(exam)
        # Add more details
        for j in range(random.randint(2, 4)):
            notes.append(f"  Additional finding: {random.choice(['Normal', 'Unremarkable', 'Within normal limits', 'No abnormalities noted'])}")
        notes.append("")
    
    # Laboratory Investigations - EXTENSIVE
    notes.append("LABORATORY INVESTIGATIONS:")
    notes.append("=" * 80)
    for i, inv in enumerate(random.sample(investigations, len(investigations)), 1):
        notes.append(f"{i}. {inv}")
        notes.append(f"   Interpretation: {random.choice(['Abnormal, clinically significant', 'Within normal limits', 'Mildly elevated', 'Consistent with diagnosis'])}")
        notes.append(f"   Clinical correlation: {random.choice(['Suggest further evaluation', 'Monitor closely', 'Repeat in 24 hours', 'Correlates with clinical picture'])}")
        notes.append("")
    
    # Additional Imaging Studies
    notes.append("ADDITIONAL IMAGING STUDIES:")
    notes.append("-" * 80)
    imaging = [
        "MRI Brain: No acute infarct, age-related white matter changes, ventricles normal size",
        "CT Abdomen/Pelvis with contrast: Hepatomegaly with fatty infiltration, spleen normal, kidneys show cortical thinning",
        "Doppler Ultrasound Lower Limbs: No evidence of deep vein thrombosis, normal venous flow bilaterally",
        "Bone Density Scan (DEXA): T-score -2.5 at lumbar spine indicating osteoporosis, recommend calcium and vitamin D",
        "Thyroid Ultrasound: Multinodular goiter, largest nodule 2.5cm in right lobe, recommend FNA biopsy"
    ]
    for img in random.sample(imaging, random.randint(2, 4)):
        notes.append(f"• {img}")
        notes.append("")
    
    # Specialist Consultations - MULTIPLE
    notes.append("SPECIALIST CONSULTATIONS:")
    notes.append("=" * 80)
    for consult in random.sample(specialist_consultations, random.randint(2, 4)):
        notes.append(consult)
        notes.append("")
    
    # Daily Progress Notes - EXTENSIVE
    notes.append("DAILY PROGRESS NOTES:")
    notes.append("=" * 80)
    for day_note in progress_notes:
        notes.append(day_note)
        # Add detailed sub-notes
        for k in range(random.randint(3, 6)):
            notes.append(f"  - {random.choice(['Vitals stable', 'Patient comfortable', 'No new complaints', 'Treatment ongoing', 'Family updated', 'Labs pending'])}")
        notes.append("")
    
    # Nursing Documentation - HOURLY
    notes.append("NURSING DOCUMENTATION:")
    notes.append("-" * 80)
    for nurse_note in nursing_notes * 3:  # Multiply to create more entries
        notes.append(nurse_note)
        notes.append("")
    
    # Multidisciplinary Team Notes
    notes.append("MULTIDISCIPLINARY TEAM NOTES:")
    notes.append("-" * 80)
    notes.append("PHYSICAL THERAPY: Patient evaluated, mobility assessment done. Ambulation with walker recommended. Strengthening exercises initiated.")
    notes.append("OCCUPATIONAL THERAPY: ADL assessment completed. Patient requires assistance with bathing and dressing. Equipment recommendations provided.")
    notes.append("DIETARY: Nutritional assessment done. Recommend high protein, low sodium diet. Caloric intake monitored. Supplements suggested.")
    notes.append("SOCIAL WORK: Psychosocial assessment completed. Patient anxious about prognosis. Counseling sessions arranged. Discharge planning initiated.")
    notes.append("PHARMACY: Medication reconciliation done. Drug interactions checked. Dosage adjustments made for renal function. Patient education provided.")
    notes.append("")
    
    # Treatment Plan - COMPREHENSIVE
    notes.append("COMPREHENSIVE TREATMENT PLAN:")
    notes.append("=" * 80)
    for i, plan in enumerate(treatment_plan, 1):
        notes.append(f"{i}. {plan}")
        notes.append(f"   Rationale: Based on current clinical presentation and diagnostic findings")
        notes.append(f"   Expected outcome: {random.choice(['Improvement in symptoms', 'Resolution of condition', 'Stabilization', 'Prevent complications'])}")
        notes.append(f"   Duration: {random.choice(['7-10 days', '2-3 weeks', 'Until clinically stable', 'As needed'])}")
        notes.append("")
    
    # Patient Education
    notes.append("PATIENT EDUCATION PROVIDED:")
    notes.append("-" * 80)
    notes.append("• Disease process and prognosis explained to patient and family in detail")
    notes.append("• Medication instructions provided with written handouts")
    notes.append("• Warning signs and symptoms to watch for discussed")
    notes.append("• Lifestyle modifications recommended including diet and exercise")
    notes.append("• Follow-up appointments scheduled and importance emphasized")
    notes.append("• Emergency contact numbers provided")
    notes.append("• Questions answered to patient's satisfaction")
    notes.append("")
    
    # Discharge Planning
    notes.append("DISCHARGE PLANNING:")
    notes.append("-" * 80)
    notes.append(f"Target discharge date: {random.randint(3, 10)} days from admission")
    notes.append("Discharge criteria: Hemodynamically stable, tolerating oral medications, adequate pain control, safe for home environment")
    notes.append("Home arrangements: Family support available, visiting nurse services arranged, medical equipment ordered")
    notes.append("Follow-up: Primary care in 1 week, specialist in 2 weeks, lab work in 3 days")
    notes.append("")
    
    # Prognosis and Long-term Plan
    notes.append("PROGNOSIS AND LONG-TERM MANAGEMENT:")
    notes.append("-" * 80)
    notes.append(f"Short-term prognosis: {random.choice(['Good with appropriate treatment', 'Guarded, close monitoring required', 'Fair, depends on compliance', 'Excellent'])}")
    notes.append(f"Long-term considerations: {random.choice(['Chronic disease management needed', 'Regular follow-up essential', 'Lifestyle modifications critical', 'Medication adherence important'])}")
    notes.append("Risk factors to address: Multiple comorbidities, medication compliance, lifestyle factors")
    notes.append("Preventive measures: Annual health screenings, immunizations up to date, regular exercise, healthy diet")
    notes.append("")
    
    # Additional padding to reach desired length
    notes.append("DETAILED CLINICAL OBSERVATIONS:")
    notes.append("-" * 80)
    for m in range(random.randint(20, 40)):
        notes.append(f"Observation #{m+1}: Patient continues to show {random.choice(['gradual improvement', 'steady progress', 'positive response to treatment', 'clinical stability'])}. "
                    f"Team will continue to monitor {random.choice(['vital signs', 'lab values', 'clinical status', 'pain levels'])} and adjust treatment as needed. "
                    f"{random.choice(['Family informed', 'Patient educated', 'Documentation updated', 'Plan reviewed with team'])}.")
    
    notes.append("")
    notes.append("=" * 80)
    notes.append("END OF COMPREHENSIVE MEDICAL RECORD")
    notes.append("=" * 80)
    notes.append("")
    notes.append(f"Total lines in this medical record: {len(notes)}")
    notes.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    notes.append("This detailed record is suitable for AI summarization into concise bullet points.")
    
    return "\n".join(notes)

def update_all_patient_notes():
    """Update all patients with comprehensive long notes"""
    with app.app_context():
        patients = Patient.query.all()
        print(f"Updating {len(patients)} patient records with comprehensive notes...\n")
        
        for i, patient in enumerate(patients, 1):
            # Generate comprehensive notes (90-1000 lines)
            comprehensive_notes = generate_comprehensive_medical_notes()
            
            # Update patient notes
            patient.notes = comprehensive_notes
            patient.generatedsummary = None  # Clear old summaries
            
            # Commit every 10 patients
            if i % 10 == 0:
                db.session.commit()
                print(f"✓ Updated {i} patients...")
        
        # Final commit
        db.session.commit()
        
        print(f"\n✓ Successfully updated all {len(patients)} patient records!")
        print("\nSample note length statistics:")
        for patient in Patient.query.limit(5).all():
            lines = patient.notes.count('\n') + 1
            print(f"  {patient.first_name} {patient.last_name}: {lines} lines, {len(patient.notes)} characters")

if __name__ == '__main__':
    print("=" * 80)
    print("UPDATING ALL PATIENT RECORDS WITH COMPREHENSIVE MEDICAL NOTES")
    print("=" * 80)
    print("\nThis will update all patient records with very detailed notes")
    print("suitable for AI summarization (90-1000 lines each).\n")
    
    update_all_patient_notes()
    
    print("\n" + "=" * 80)
    print("UPDATE COMPLETE!")
    print("=" * 80)
