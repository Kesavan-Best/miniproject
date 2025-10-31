from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
try:
    import google.generativeai as genai
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

app = Flask(__name__)
app.config['SECRET_KEY'] = '52c487cd4bddb0c95bbf851a7ef2fe6689410f37cc2792e9'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'site.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    primary_diagnosis = db.Column(db.String(200), nullable=False)
    attending_physician = db.Column(db.String(100), nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    generatedsummary = db.Column(db.Text)

    def __repr__(self):
        return f"Patient('{self.first_name} {self.last_name}', '{self.primary_diagnosis}')"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            patients = Patient.query.all()
            for patient in patients:
                patient.generatedsummary = None
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/api/patient/<int:patient_id>/summary', methods=['DELETE'])
@login_required
def delete_patient_summary(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.generatedsummary = None
    db.session.commit()
    return jsonify({'message': 'Summary deleted.'})

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', title='Dashboard', patients=patients)

GEMINI_API_KEY = "AIzaSyAdqpeBM2zVqGrbRHSxRnFoalpQiERzGB4"
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("Gemini API key not set. Please set the GEMINI_API_KEY variable in code or environment.")
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/api/patient/<int:patient_id>', methods=['GET'])
@login_required
def get_patient_notes(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({'notes': patient.notes or ''})

@app.route('/api/patient/<int:patient_id>/generate_summary', methods=['POST'])
@login_required
def generate_patient_summary(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    notes = patient.notes or ''
    if not notes.strip():
        return jsonify({"message": "No notes available to summarize.", "generatedsummary": ""}), 400
    try:
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""Summarize the following comprehensive medical notes into 3-4 concise bullet points. 
        Format your response as bullet points using • symbol.
        Each bullet point should be a complete sentence capturing key medical information.
        Focus on: diagnosis, key findings, treatment plan, and patient status.
        Only use information from the notes provided. Do not add any information not present in the notes.
        
        Medical Notes:
        {notes}"""
        response = gemini_model.generate_content([prompt])
        print(f"Gemini API response: {response}")
        summary = None
        if hasattr(response, 'text') and response.text:
            summary = response.text
        elif hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'text') and candidate.text:
                summary = candidate.text
            elif hasattr(candidate, 'parts') and candidate.parts:
                summary = str(candidate.parts[0])
        elif hasattr(response, 'parts') and response.parts:
            summary = str(response.parts[0])
        if not summary or not summary.strip():
            return jsonify({"message": "Gemini API did not return a summary.", "generatedsummary": ""}), 500
        patient.generatedsummary = summary.strip()
        db.session.commit()
        return jsonify({"message": "Summary generated.", "generatedsummary": summary.strip()})
    except Exception as e:
        print(f"Error generating summary: {e}")
        return jsonify({"message": f"Error generating summary: {e}", "generatedsummary": ""}), 500

@app.route('/api/patient/<int:patient_id>/summary', methods=['GET'])
@login_required
def get_patient_summary(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({'generatedsummary': patient.generatedsummary or ''})

@app.route('/api/patients', methods=['GET', 'POST'])
@login_required
def api_patients():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            if not data.get('first_name') or not data.get('last_name') or not data.get('primary_diagnosis'):
                return jsonify({'error': 'Missing required fields: first_name, last_name, primary_diagnosis'}), 400
            
            try:
                dob = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None
                adm = datetime.strptime(data.get('admission_date'), '%Y-%m-%d').date() if data.get('admission_date') else None
                if not dob or not adm:
                    return jsonify({'error': 'Date of Birth and Admission Date are required'}), 400
            except ValueError as e:
                return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
            
            patient = Patient(
                first_name=data.get('first_name').strip(),
                last_name=data.get('last_name').strip(),
                date_of_birth=dob,
                gender=data.get('gender', '').strip(),
                contact_number=data.get('contact_number', '').strip(),
                email=data.get('email', '').strip() if data.get('email') else None,
                primary_diagnosis=data.get('primary_diagnosis').strip(),
                attending_physician=data.get('attending_physician', '').strip(),
                admission_date=adm,
                status=data.get('status', 'admitted').strip(),
                notes=data.get('notes', '')
            )
            
            db.session.add(patient)
            db.session.commit()
            
            return jsonify({
                'message': 'Patient created successfully',
                'patient': {
                    'id': patient.id,
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
                    'gender': patient.gender,
                    'contact_number': patient.contact_number,
                    'email': patient.email,
                    'primary_diagnosis': patient.primary_diagnosis,
                    'attending_physician': patient.attending_physician,
                    'admission_date': patient.admission_date.strftime('%Y-%m-%d'),
                    'status': patient.status,
                    'notes': patient.notes or ''
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating patient: {str(e)}")
            return jsonify({'error': f'Server error: {str(e)}'}), 500
    
    patients = Patient.query.all()
    print(f"Fetched {len(patients)} patients from the database.")

    seen = set()
    unique_patients = []

    def serialize(patient):
        return {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else '',
            'gender': patient.gender,
            'contact_number': patient.contact_number,
            'email': patient.email,
            'primary_diagnosis': patient.primary_diagnosis,
            'attending_physician': patient.attending_physician,
            'admission_date': patient.admission_date.strftime('%Y-%m-%d') if patient.admission_date else '',
            'status': patient.status,
            'notes': patient.notes or ''
        }

    for p in patients:
        key = (p.first_name.strip().lower() if p.first_name else '', p.last_name.strip().lower() if p.last_name else '')
        if key in seen:
            continue
        seen.add(key)
        unique_patients.append(serialize(p))

    return jsonify({'patients': unique_patients})

@app.route('/api/patient/<int:patient_id>/status', methods=['PUT'])
@login_required
def update_patient_status(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        
        patient.status = data.get('status', patient.status)
        
        if data.get('notes'):
            if patient.notes:
                patient.notes += f"\n\nStatus Update: {data.get('notes')}"
            else:
                patient.notes = f"Status Update: {data.get('notes')}"
        
        db.session.commit()
        
        return jsonify({
            'message': 'Patient status updated successfully',
            'patient': {
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'status': patient.status
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/<int:patient_id>', methods=['PUT'])
@login_required
def update_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if not data.get('first_name') or not data.get('last_name') or not data.get('primary_diagnosis'):
            return jsonify({'error': 'Missing required fields: first_name, last_name, primary_diagnosis'}), 400

        patient.first_name = data.get('first_name', patient.first_name).strip()
        patient.last_name = data.get('last_name', patient.last_name).strip()
        patient.gender = data.get('gender', patient.gender).strip()
        patient.contact_number = data.get('contact_number', patient.contact_number).strip()
        patient.email = data.get('email', patient.email).strip() if data.get('email') else patient.email
        patient.primary_diagnosis = data.get('primary_diagnosis', patient.primary_diagnosis).strip()
        patient.attending_physician = data.get('attending_physician', patient.attending_physician).strip()
        patient.status = data.get('status', patient.status).strip()
        patient.notes = data.get('notes', patient.notes)

        dob_str = data.get('date_of_birth')
        if dob_str and dob_str.strip():
            try:
                patient.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError as e:
                return jsonify({'error': f'Invalid date format for DOB: {str(e)}'}), 400

        adm_str = data.get('admission_date')
        if adm_str and adm_str.strip():
            try:
                patient.admission_date = datetime.strptime(adm_str, '%Y-%m-%d').date()
            except ValueError as e:
                return jsonify({'error': f'Invalid date format for admission date: {str(e)}'}), 400

        db.session.commit()

        def fmt_date(d):
            return d.strftime('%Y-%m-%d') if d else ''

        return jsonify({
            'message': 'Patient updated successfully',
            'patient': {
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'date_of_birth': fmt_date(patient.date_of_birth),
                'gender': patient.gender,
                'contact_number': patient.contact_number,
                'email': patient.email,
                'primary_diagnosis': patient.primary_diagnosis,
                'attending_physician': patient.attending_physician,
                'admission_date': fmt_date(patient.admission_date),
                'status': patient.status,
                'notes': patient.notes
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating patient: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def add_sample_patients():
    sample_patients = [
        Patient(
            first_name="John",
            last_name="Smith",
            date_of_birth=datetime(1985, 5, 15).date(),
            gender="male",
            contact_number="555-0101",
            email="john.smith@email.com",
            primary_diagnosis="Hypertension",
            attending_physician="Dr. Sarah Wilson",
            admission_date=datetime(2024, 1, 10).date(),
            status="admitted",
            notes="Patient presented with elevated blood pressure. Prescribed medication and lifestyle changes."
        ),
        Patient(
            first_name="Maria",
            last_name="Garcia",
            date_of_birth=datetime(1978, 8, 22).date(),
            gender="female",
            contact_number="555-0102",
            email="maria.garcia@email.com",
            primary_diagnosis="Type 2 Diabetes",
            attending_physician="Dr. Michael Chen",
            admission_date=datetime(2024, 1, 12).date(),
            status="observation",
            notes="Monitoring blood sugar levels. Patient educated about diet and exercise."
        ),
        Patient(
            first_name="David",
            last_name="Johnson",
            date_of_birth=datetime(1992, 3, 8).date(),
            gender="male",
            contact_number="555-0103",
            email="david.johnson@email.com",
            primary_diagnosis="Appendicitis",
            attending_physician="Dr. Emily Brown",
            admission_date=datetime(2024, 1, 14).date(),
            status="emergency",
            notes="Emergency surgery performed. Patient recovering well in post-op care."
        ),
        Patient(
            first_name="Sarah",
            last_name="Williams",
            date_of_birth=datetime(1980, 11, 30).date(),
            gender="female",
            contact_number="555-0104",
            email="sarah.williams@email.com",
            primary_diagnosis="Pneumonia",
            attending_physician="Dr. James Taylor",
            admission_date=datetime(2024, 1, 8).date(),
            status="discharged",
            notes="Completed antibiotic course. Follow-up appointment scheduled in 2 weeks."
        )
    ]
    
    existing_count = Patient.query.count()
    if existing_count == 0:
        for patient in sample_patients:
            db.session.add(patient)
        db.session.commit()
        print("Sample patient data added successfully!")
    else:
        print(f"Database already contains {existing_count} patients. Skipping sample data.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_patients()
    app.run(debug=True)