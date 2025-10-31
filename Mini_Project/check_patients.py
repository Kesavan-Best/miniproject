from app import app, db, Patient

with app.app_context():
    total = Patient.query.count()
    admitted = Patient.query.filter_by(status='admitted').count()
    observation = Patient.query.filter_by(status='observation').count()
    appointment = Patient.query.filter_by(status='appointment').count()
    emergency = Patient.query.filter_by(status='emergency').count()
    discharged = Patient.query.filter_by(status='discharged').count()
    
    print("=" * 50)
    print("PATIENT DATABASE STATISTICS")
    print("=" * 50)
    print(f"Total patients: {total}")
    print(f"Admitted: {admitted}")
    print(f"Observation: {observation}")
    print(f"Appointment: {appointment}")
    print(f"Emergency: {emergency}")
    print(f"Discharged: {discharged}")
    print("=" * 50)
    
    # Show a few sample patients
    print("\nSample Patient Records:")
    print("=" * 50)
    sample_patients = Patient.query.limit(5).all()
    for p in sample_patients:
        print(f"\n{p.first_name} {p.last_name}")
        print(f"  Diagnosis: {p.primary_diagnosis}")
        print(f"  Status: {p.status}")
        print(f"  Physician: {p.attending_physician}")
