#!/usr/bin/env python3
"""Add tabindex to all form fields in dashboard.html for proper Tab key navigation"""

import re

# Read the dashboard.html file
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the form fields in Add Patient Modal with their tabindex
add_patient_fields = [
    ('id="addFirstName"', 'id="addFirstName" tabindex="1"'),
    ('id="addLastName"', 'id="addLastName" tabindex="2"'),
    ('id="addDob"', 'id="addDob" tabindex="3"'),
    ('id="addGender"', 'id="addGender" tabindex="4"'),
    ('id="addContact"', 'id="addContact" tabindex="5"'),
    ('id="addEmail"', 'id="addEmail" tabindex="6"'),
    ('id="addDiagnosis"', 'id="addDiagnosis" tabindex="7"'),
    ('id="addPhysician"', 'id="addPhysician" tabindex="8"'),
    ('id="addAdmissionDate"', 'id="addAdmissionDate" tabindex="9"'),
    ('id="addStatus"', 'id="addStatus" tabindex="10"'),
    ('id="addNotes"', 'id="addNotes" tabindex="11"'),
]

# Define the form fields in Edit Patient Modal with their tabindex
edit_patient_fields = [
    ('id="editFirstName"', 'id="editFirstName" tabindex="1"'),
    ('id="editLastName"', 'id="editLastName" tabindex="2"'),
    ('id="editDob"', 'id="editDob" tabindex="3"'),
    ('id="editGender"', 'id="editGender" tabindex="4"'),
    ('id="editContact"', 'id="editContact" tabindex="5"'),
    ('id="editEmail"', 'id="editEmail" tabindex="6"'),
    ('id="editDiagnosis"', 'id="editDiagnosis" tabindex="7"'),
    ('id="editPhysician"', 'id="editPhysician" tabindex="8"'),
    ('id="editAdmissionDate"', 'id="editAdmissionDate" tabindex="9"'),
    ('id="editStatus"', 'id="editStatus" tabindex="10"'),
    ('id="editNotes"', 'id="editNotes" tabindex="11"'),
]

# Apply replacements for Add Patient form
for old, new in add_patient_fields:
    # Only replace if tabindex not already present
    if old in content and 'tabindex' not in content[content.find(old):content.find(old)+100]:
        content = content.replace(old + ' required', new + ' required', 1)
        content = content.replace(old + '>', new + '>', 1)
        print(f"✓ Added tabindex to {old}")

# Apply replacements for Edit Patient form
for old, new in edit_patient_fields:
    # Only replace if tabindex not already present
    if old in content and 'tabindex' not in content[content.find(old):content.find(old)+100]:
        content = content.replace(old + ' required', new + ' required', 1)
        content = content.replace(old + '>', new + '>', 1)
        print(f"✓ Added tabindex to {old}")

# Write back the modified content
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ Successfully added tabindex to all form fields!")
print("✓ Users can now use Tab key to navigate between fields in Add/Edit Patient forms")
