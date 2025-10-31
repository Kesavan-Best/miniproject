// Dashboard JavaScript - Fixed Patient Forms
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized - Lavender Theme');
    
    // Initialize modals
    const editPatientModal = new bootstrap.Modal(document.getElementById('editPatientModal'));
    const addPatientModal = new bootstrap.Modal(document.getElementById('addPatientModal'));
    const summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
    const notesModal = new bootstrap.Modal(document.getElementById('notesModal'));
    
    // Global variables
    let currentPatientId = null;
    let patientsData = [];
    
    // Initialize dashboard
    initializeDashboard();
    
    // Event Listeners - FIXED: Proper event binding
    document.getElementById('openAddPatientBtn').addEventListener('click', openAddPatientModal);
    document.getElementById('saveNewPatient').addEventListener('click', saveNewPatient);
    document.getElementById('savePatientChanges').addEventListener('click', savePatientChanges);
    document.getElementById('searchInput').addEventListener('input', filterPatients);
    document.getElementById('regenerateSummary').addEventListener('click', function() {
        if (currentPatientId) {
            generateSummary(currentPatientId);
        }
    });
    
    // Initialize dashboard data
    function initializeDashboard() {
        console.log('Loading dashboard data...');
        loadPatients();
    }
    
    // Load patients data
    function loadPatients() {
        console.log('Loading patients...');
        
        // Show loading state
        const tableBody = document.getElementById('patientsTableBody');
        tableBody.innerHTML = `
            <tr class="loading-row">
                <td colspan="3">
                    <div class="loading-spinner">
                        <i class="fas fa-spinner fa-spin"></i>
                        <span>Loading patient data...</span>
                    </div>
                </td>
            </tr>
        `;
        
        // Simulate API call with timeout
        setTimeout(() => {
            // Sample data with proper status distribution
            patientsData = [
                {
                    id: 1,
                    firstName: 'John',
                    lastName: 'Doe',
                    dob: '1985-03-15',
                    gender: 'male',
                    contact: '+1-555-0123',
                    email: 'john.doe@email.com',
                    diagnosis: 'Hypertension',
                    physician: 'Dr. Smith',
                    admissionDate: '2024-01-15',
                    status: 'admitted',
                    notes: 'Patient shows improvement in blood pressure levels. Continue current medication.'
                },
                {
                    id: 2,
                    firstName: 'Jane',
                    lastName: 'Smith',
                    dob: '1978-07-22',
                    gender: 'female',
                    contact: '+1-555-0124',
                    email: 'jane.smith@email.com',
                    diagnosis: 'Diabetes Type 2',
                    physician: 'Dr. Johnson',
                    admissionDate: '2024-01-20',
                    status: 'observation',
                    notes: 'Blood sugar levels stabilizing. Monitor diet closely.'
                },
                {
                    id: 3,
                    firstName: 'Robert',
                    lastName: 'Brown',
                    dob: '1990-11-30',
                    gender: 'male',
                    contact: '+1-555-0125',
                    email: 'robert.b@email.com',
                    diagnosis: 'Pneumonia',
                    physician: 'Dr. Williams',
                    admissionDate: '2024-01-25',
                    status: 'emergency',
                    notes: 'Severe respiratory symptoms. Administer antibiotics and monitor oxygen levels.'
                },
                {
                    id: 4,
                    firstName: 'Sarah',
                    lastName: 'Johnson',
                    dob: '1982-05-14',
                    gender: 'female',
                    contact: '+1-555-0126',
                    email: 'sarah.j@email.com',
                    diagnosis: 'Appendicitis',
                    physician: 'Dr. Davis',
                    admissionDate: '2024-01-28',
                    status: 'discharged',
                    notes: 'Post-surgery recovery. Patient discharged with follow-up instructions.'
                }
            ];
            
            renderPatientsTable(patientsData);
            updateStatistics();
        }, 1000);
    }
    
    // Render patients table
    function renderPatientsTable(patients) {
        const tableBody = document.getElementById('patientsTableBody');
        
        if (patients.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center py-5">
                        <div class="empty-state">
                            <i class="fas fa-user-slash"></i>
                            <h5>No patients found</h5>
                            <p>Try adjusting your search criteria</p>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }
        
        tableBody.innerHTML = patients.map(patient => `
            <tr class="patient-row" data-patient-id="${patient.id}">
                <td>
                    <div class="patient-info-cell">
                        <div class="patient-avatar">
                            ${patient.firstName.charAt(0)}${patient.lastName.charAt(0)}
                        </div>
                        <div class="patient-details">
                            <div class="patient-name">${patient.firstName} ${patient.lastName}</div>
                            <div class="patient-meta">
                                <strong>Diagnosis:</strong> ${patient.diagnosis} | 
                                <strong>Physician:</strong> ${patient.physician}<br>
                                <strong>DOB:</strong> ${formatDate(patient.dob)} | 
                                <strong>Contact:</strong> ${patient.contact}
                            </div>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="status-display">
                        <select class="form-select status-dropdown" data-patient-id="${patient.id}">
                            <option value="admitted" ${patient.status === 'admitted' ? 'selected' : ''}>Admitted</option>
                            <option value="observation" ${patient.status === 'observation' ? 'selected' : ''}>Observation</option>
                            <option value="appointment" ${patient.status === 'appointment' ? 'selected' : ''}>Appointment</option>
                            <option value="emergency" ${patient.status === 'emergency' ? 'selected' : ''}>Emergency</option>
                            <option value="discharged" ${patient.status === 'discharged' ? 'selected' : ''}>Discharged</option>
                        </select>
                        <button class="btn btn-status-edit" onclick="updatePatientStatus(${patient.id})" title="Update Status">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-action btn-notes" onclick="viewNotes(${patient.id})" title="View Notes">
                            <i class="fas fa-file-medical"></i>
                        </button>
                        <button class="btn-action btn-summary" onclick="generateSummary(${patient.id})" title="Generate Summary">
                            <i class="fas fa-file-medical-alt"></i>
                        </button>
                        <button class="btn-action btn-edit" onclick="editPatient(${patient.id})" title="Edit Patient">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-action btn-delete" onclick="deletePatient(${patient.id})" title="Delete Patient">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
        
        // Add event listeners to status dropdowns
        document.querySelectorAll('.status-dropdown').forEach(dropdown => {
            dropdown.addEventListener('change', function() {
                const patientId = this.getAttribute('data-patient-id');
                updatePatientStatus(parseInt(patientId));
            });
        });
    }
    
    // Update statistics - FIXED COUNTING
    function updateStatistics() {
        console.log('Updating statistics...');
        
        // Count patients by status
        const stats = {
            total: patientsData.length,
            admitted: patientsData.filter(p => p.status === 'admitted').length,
            appointment: patientsData.filter(p => p.status === 'appointment').length,
            observation: patientsData.filter(p => p.status === 'observation').length,
            emergency: patientsData.filter(p => p.status === 'emergency').length,
            discharged: patientsData.filter(p => p.status === 'discharged').length
        };
        
        console.log('Statistics calculated:', stats);
        
        // Update UI with animation
        animateCounter('totalPatients', stats.total);
        animateCounter('admittedPatients', stats.admitted);
        animateCounter('appointmentPatients', stats.appointment);
        animateCounter('observationPatients', stats.observation);
        animateCounter('emergencyPatients', stats.emergency);
        animateCounter('dischargedPatients', stats.discharged);
    }
    
    // Animate counter values
    function animateCounter(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        let current = 0;
        const increment = targetValue / 20;
        const timer = setInterval(() => {
            current += increment;
            if (current >= targetValue) {
                element.textContent = targetValue;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 50);
    }
    
    // Filter patients based on search input
    function filterPatients() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        
        if (!searchTerm) {
            renderPatientsTable(patientsData);
            return;
        }
        
        const filteredPatients = patientsData.filter(patient => 
            patient.firstName.toLowerCase().includes(searchTerm) ||
            patient.lastName.toLowerCase().includes(searchTerm) ||
            patient.diagnosis.toLowerCase().includes(searchTerm) ||
            patient.physician.toLowerCase().includes(searchTerm) ||
            patient.contact.includes(searchTerm) ||
            patient.status.toLowerCase().includes(searchTerm)
        );
        
        renderPatientsTable(filteredPatients);
    }
    
    // Open add patient modal - FIXED: Proper modal opening
    function openAddPatientModal() {
        console.log('Opening add patient modal...');
        
        // Reset form and clear any previous values
        const form = document.getElementById('addPatientForm');
        if (form) {
            form.reset();
        }
        
        // Set default values
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('addAdmissionDate').value = today;
        document.getElementById('addStatus').value = 'admitted';
        
        // Show modal
        addPatientModal.show();
        
        // Focus on first field
        setTimeout(() => {
            const firstNameField = document.getElementById('addFirstName');
            if (firstNameField) {
                firstNameField.focus();
            }
        }, 500);
    }
    
    // Save new patient - FIXED: Proper form handling
    function saveNewPatient(event) {
        if (event) event.preventDefault();
        
        console.log('Saving new patient...');
        
        const form = document.getElementById('addPatientForm');
        
        // Basic validation
        const requiredFields = [
            'addFirstName', 'addLastName', 'addDob', 'addGender', 
            'addContact', 'addDiagnosis', 'addPhysician', 'addAdmissionDate'
        ];
        
        let isValid = true;
        let errorMessage = '';
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#dc3545';
                errorMessage = 'Please fill in all required fields';
            } else {
                field.style.borderColor = '';
            }
        });
        
        if (!isValid) {
            showNotification(errorMessage, 'error');
            return;
        }
        
        // Create new patient object
        const newPatient = {
            id: patientsData.length > 0 ? Math.max(...patientsData.map(p => p.id)) + 1 : 1,
            firstName: document.getElementById('addFirstName').value.trim(),
            lastName: document.getElementById('addLastName').value.trim(),
            dob: document.getElementById('addDob').value,
            gender: document.getElementById('addGender').value,
            contact: document.getElementById('addContact').value.trim(),
            email: document.getElementById('addEmail').value.trim(),
            diagnosis: document.getElementById('addDiagnosis').value.trim(),
            physician: document.getElementById('addPhysician').value.trim(),
            admissionDate: document.getElementById('addAdmissionDate').value,
            status: document.getElementById('addStatus').value,
            notes: document.getElementById('addNotes').value.trim()
        };
        
        console.log('New patient data:', newPatient);
        
        // Add to patients array
        patientsData.push(newPatient);
        
        // Update UI
        renderPatientsTable(patientsData);
        updateStatistics();
        
        // Close modal
        addPatientModal.hide();
        
        // Show success message
        showNotification(`Patient ${newPatient.firstName} ${newPatient.lastName} added successfully!`, 'success');
    }
    
    // Edit patient - FIXED: Proper patient data loading
    window.editPatient = function(patientId) {
        console.log('Editing patient:', patientId);
        
        const patient = patientsData.find(p => p.id === patientId);
        
        if (!patient) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        currentPatientId = patientId;
        
        // Populate form with patient data
        document.getElementById('editPatientId').value = patient.id;
        document.getElementById('editFirstName').value = patient.firstName;
        document.getElementById('editLastName').value = patient.lastName;
        document.getElementById('editDob').value = patient.dob;
        document.getElementById('editGender').value = patient.gender;
        document.getElementById('editContact').value = patient.contact;
        document.getElementById('editEmail').value = patient.email || '';
        document.getElementById('editDiagnosis').value = patient.diagnosis;
        document.getElementById('editPhysician').value = patient.physician;
        document.getElementById('editAdmissionDate').value = patient.admissionDate;
        document.getElementById('editStatus').value = patient.status;
        document.getElementById('editNotes').value = patient.notes || '';
        
        console.log('Form populated with patient data');
        
        // Show modal
        editPatientModal.show();
        
        // Focus on first field
        setTimeout(() => {
            const firstNameField = document.getElementById('editFirstName');
            if (firstNameField) {
                firstNameField.focus();
            }
        }, 500);
    };
    
    // Save patient changes - FIXED: Proper update handling
    function savePatientChanges(event) {
        if (event) event.preventDefault();
        
        console.log('Saving patient changes for ID:', currentPatientId);
        
        const form = document.getElementById('editPatientForm');
        
        // Basic validation
        const requiredFields = [
            'editFirstName', 'editLastName', 'editDob', 'editGender', 
            'editContact', 'editDiagnosis', 'editPhysician', 'editAdmissionDate'
        ];
        
        let isValid = true;
        let errorMessage = '';
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#dc3545';
                errorMessage = 'Please fill in all required fields';
            } else {
                field.style.borderColor = '';
            }
        });
        
        if (!isValid) {
            showNotification(errorMessage, 'error');
            return;
        }
        
        const patientIndex = patientsData.findIndex(p => p.id === currentPatientId);
        
        if (patientIndex === -1) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        // Update patient data
        patientsData[patientIndex] = {
            ...patientsData[patientIndex],
            firstName: document.getElementById('editFirstName').value.trim(),
            lastName: document.getElementById('editLastName').value.trim(),
            dob: document.getElementById('editDob').value,
            gender: document.getElementById('editGender').value,
            contact: document.getElementById('editContact').value.trim(),
            email: document.getElementById('editEmail').value.trim(),
            diagnosis: document.getElementById('editDiagnosis').value.trim(),
            physician: document.getElementById('editPhysician').value.trim(),
            admissionDate: document.getElementById('editAdmissionDate').value,
            status: document.getElementById('editStatus').value,
            notes: document.getElementById('editNotes').value.trim()
        };
        
        console.log('Patient updated:', patientsData[patientIndex]);
        
        // Update UI
        renderPatientsTable(patientsData);
        updateStatistics();
        
        // Close modal
        editPatientModal.hide();
        
        // Show success message
        showNotification('Patient updated successfully!', 'success');
    }
    
    // Update patient status
    window.updatePatientStatus = function(patientId) {
        const patientIndex = patientsData.findIndex(p => p.id === patientId);
        
        if (patientIndex === -1) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        const dropdown = document.querySelector(`.status-dropdown[data-patient-id="${patientId}"]`);
        const newStatus = dropdown.value;
        
        patientsData[patientIndex].status = newStatus;
        updateStatistics();
        
        showNotification(`Patient status updated to ${newStatus}`, 'success');
    };
    
    // View patient notes
    window.viewNotes = function(patientId) {
        const patient = patientsData.find(p => p.id === patientId);
        
        if (!patient) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        document.getElementById('notesText').textContent = 
            patient.notes || 'No notes available for this patient.';
        
        notesModal.show();
    };
    
    // Generate AI summary
    window.generateSummary = function(patientId) {
        const patient = patientsData.find(p => p.id === patientId);
        
        if (!patient) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        currentPatientId = patientId;
        
        // Show loading state
        document.getElementById('summaryLoading').style.display = 'block';
        document.getElementById('summaryContent').style.display = 'none';
        document.getElementById('summaryError').style.display = 'none';
        
        // Update patient info in modal
        document.getElementById('summaryPatientName').textContent = 
            `${patient.firstName} ${patient.lastName}`;
        document.getElementById('summaryStatus').textContent = 
            patient.status.charAt(0).toUpperCase() + patient.status.slice(1);
        
        summaryModal.show();
        
        // Simulate AI summary generation
        setTimeout(() => {
            document.getElementById('summaryLoading').style.display = 'none';
            document.getElementById('summaryContent').style.display = 'block';
            
            const summary = generateAISummary(patient);
            document.getElementById('summaryText').textContent = summary;
        }, 2000);
    };
    
    // Generate AI summary content
    function generateAISummary(patient) {
        const statusMap = {
            'admitted': 'currently admitted',
            'observation': 'under observation',
            'appointment': 'scheduled for appointment',
            'emergency': 'in emergency care',
            'discharged': 'discharged'
        };
        
        const genderPronoun = patient.gender === 'female' ? 'She' : 'He';
        const possessivePronoun = patient.gender === 'female' ? 'Her' : 'His';
        
        return `PATIENT SUMMARY: ${patient.firstName} ${patient.lastName}

OVERVIEW:
${patient.firstName} ${patient.lastName} is ${statusMap[patient.status]} at MedCare Hospital.
${possessivePronoun} primary diagnosis is ${patient.diagnosis}, under the care of ${patient.physician}.

DEMOGRAPHICS:
• Age: ${calculateAge(patient.dob)} years
• Gender: ${patient.gender.charAt(0).toUpperCase() + patient.gender.slice(1)}
• Contact: ${patient.contact}${patient.email ? ` | Email: ${patient.email}` : ''}
• Admission Date: ${formatDate(patient.admissionDate)}
• Current Status: ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}

MEDICAL NOTES:
${patient.notes || 'No additional medical notes available at this time.'}

RECOMMENDATIONS:
${getRecommendationsBasedOnStatus(patient.status)}

This AI-generated summary was created on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}.`;
    }
    
    // Delete patient
    window.deletePatient = function(patientId) {
        const patient = patientsData.find(p => p.id === patientId);
        if (!patient) {
            showNotification('Patient not found!', 'error');
            return;
        }
        
        const patientName = `${patient.firstName} ${patient.lastName}`;
        
        if (!confirm(`Are you sure you want to delete patient ${patientName}? This action cannot be undone.`)) {
            return;
        }
        
        const patientIndex = patientsData.findIndex(p => p.id === patientId);
        
        patientsData.splice(patientIndex, 1);
        renderPatientsTable(patientsData);
        updateStatistics();
        
        showNotification(`Patient ${patientName} deleted successfully!`, 'success');
    };
    
    // Utility functions
    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    function calculateAge(dob) {
        const birthDate = new Date(dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        
        return age;
    }
    
    function getRecommendationsBasedOnStatus(status) {
        const recommendations = {
            'admitted': '- Continue current treatment plan\n- Monitor vital signs regularly\n- Schedule follow-up assessments\n- Coordinate with nursing staff',
            'observation': '- Monitor symptoms closely\n- Maintain regular check-ins\n- Adjust treatment as needed\n- Document any changes',
            'appointment': '- Prepare for upcoming consultation\n- Review medical history\n- Note any new symptoms\n- Confirm appointment details',
            'emergency': '- Provide immediate care as needed\n- Monitor critical indicators\n- Prepare for possible procedures\n- Alert specialist if required',
            'discharged': '- Follow discharge instructions\n- Schedule follow-up appointment\n- Monitor recovery progress\n- Provide patient education materials'
        };
        
        return recommendations[status] || '- Follow standard care protocols';
    }
    
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 5px 15px rgba(150, 123, 182, 0.3);
            border-radius: 12px;
            border: none;
            border-left: 4px solid ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#967bb6'};
        `;
        
        const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle';
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${icon} me-2"></i>
                <span>${message}</span>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
});