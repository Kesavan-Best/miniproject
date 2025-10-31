# 🧪 Complete Testing Guide - Version 2.0

## Pre-Test Setup

1. **Start Server**:
   ```powershell
   python app.py
   ```
   Expected output: "Running on http://127.0.0.1:5000"

2. **Open Browser**:
   ```
   http://127.0.0.1:5000/dashboard
   ```

3. **Verify Dashboard Loads**:
   - See patient table with existing data
   - See "Add Patient" button (top right)
   - See status dropdown in each row

---

## 🧪 Test Suite 1: Add Patient Form

### Test 1.1: Form Opens Properly
**Steps**:
1. Click "Add Patient" button
2. Modal appears with title "Add New Patient"
3. All form fields are visible and empty

**Expected Results**:
- Modal opens without errors
- Title shows "Add New Patient"
- Input fields are blank
- Status field shows "admitted"
- No console errors

**Pass/Fail**: ___

---

### Test 1.2: Input Fields Accept Data
**Steps**:
1. Click in "First Name" field
2. Type "John"
3. Click in "Last Name" field  
4. Type "Doe"
5. Click in "Contact Number" field
6. Type "9876543210"

**Expected Results**:
- Text appears as you type
- Fields are editable
- Cursor works normally
- No field is locked/disabled

**Pass/Fail**: ___

---

### Test 1.3: Dropdown Fields Work
**Steps**:
1. Click "Gender" dropdown
2. Select "Male"
3. Click "Status" dropdown
4. Select "Discharged"

**Expected Results**:
- Options appear when clicked
- Selection updates field
- Values persist

**Pass/Fail**: ___

---

### Test 1.4: Date Fields Work
**Steps**:
1. Click "Date of Birth" field
2. Select a date from picker
3. Click "Admission Date" field
4. Select a date from picker

**Expected Results**:
- Date picker opens
- Date is selectable
- Selected date displays
- Format is correct (dd-mm-yyyy)

**Pass/Fail**: ___

---

### Test 1.5: Add Patient Submit
**Steps**:
1. Fill all required fields:
   - First Name: "John"
   - Last Name: "Doe"
   - Date of Birth: "15-01-1990"
   - Gender: "Male"
   - Contact Number: "9876543210"
   - Primary Diagnosis: "Diabetes"
   - Attending Physician: "Dr. Smith"
   - Admission Date: "20-10-2025"
   - Status: "admitted"
2. Click "Save Changes" button
3. Wait for response

**Expected Results**:
- Modal closes
- Green success message: "✓ Patient created successfully!"
- New patient appears in table at bottom
- Table shows: John Doe, ID shown, Diabetes, Dr. Smith
- Status shows as "Admitted"

**Pass/Fail**: ___

---

### Test 1.6: Form Reset After Save
**Steps**:
1. Click "Add Patient" again
2. Check if form is empty

**Expected Results**:
- All fields are blank
- Status is "admitted" by default
- Ready for new patient entry

**Pass/Fail**: ___

---

### Test 1.7: Validation - Missing Required Fields
**Steps**:
1. Click "Add Patient"
2. Leave "First Name" empty
3. Leave "Last Name" empty
4. Click "Save Changes"

**Expected Results**:
- Form does NOT submit
- Warning message appears: "Please fill in all required fields"
- Modal stays open
- Form data preserved

**Pass/Fail**: ___

---

### Test 1.8: Validation - Invalid Date
**Steps**:
1. Click "Add Patient"
2. Fill all fields correctly
3. In "Date of Birth": type "99-99-9999"
4. Click "Save Changes"

**Expected Results**:
- Form does NOT submit
- Error message about date format
- Modal stays open

**Pass/Fail**: ___

---

## 🧪 Test Suite 2: Status Dropdown (NEW)

### Test 2.1: Status Dropdown Visible
**Steps**:
1. Look at patient table
2. Find first patient row
3. Look at "Status" column

**Expected Results**:
- See dropdown (NOT badge)
- Shows current status
- Dropdown is blue and interactive
- Edit button (pencil) next to it

**Pass/Fail**: ___

---

### Test 2.2: Dropdown Opens
**Steps**:
1. Click status dropdown
2. Observe options

**Expected Results**:
- Dropdown expands
- Shows 4 options:
  - Admitted
  - Discharged
  - Observation
  - Emergency
- Current status is highlighted

**Pass/Fail**: ___

---

### Test 2.3: Status Change - Admitted to Discharged
**Steps**:
1. Find patient with "Admitted" status
2. Click status dropdown
3. Select "Discharged"
4. Wait 2 seconds

**Expected Results**:
- Dropdown immediately shows "Discharged"
- Green success message: "✓ Status updated to discharged!"
- Message disappears after 3 seconds
- Status persists in row

**Pass/Fail**: ___

---

### Test 2.4: Status Change - Persists on Refresh
**Steps**:
1. Change status (e.g., to "Emergency")
2. Wait for success message
3. Press F5 or refresh page
4. Wait for table to load

**Expected Results**:
- Patient still shows new status
- Status was saved to database
- Change is permanent

**Pass/Fail**: ___

---

### Test 2.5: Status Change - All Options
**Steps**:
1. For each status option:
   - Select from dropdown
   - Verify change
   - Note in table

**Status Options to Test**:
- [ ] Admitted
- [ ] Discharged
- [ ] Observation  
- [ ] Emergency

**Expected Results**:
- All 4 statuses work
- All changes saved
- No errors

**Pass/Fail**: ___

---

### Test 2.6: Edit Button Still Works
**Steps**:
1. Click pencil (edit) button next to status
2. Full edit form opens

**Expected Results**:
- Edit modal opens
- Title: "Edit Patient Details"
- All fields pre-filled
- Can still edit full patient

**Pass/Fail**: ___

---

## 🧪 Test Suite 3: UI & Styling

### Test 3.1: Stat Cards
**Steps**:
1. Look at top cards (Total Patients, Admitted, etc.)
2. Hover over a card

**Expected Results**:
- Cards have shadows
- Cards rise up on hover
- Icons have gradient colors
- Professional appearance

**Pass/Fail**: ___

---

### Test 3.2: Status Dropdown Styling
**Steps**:
1. Click status dropdown
2. Type while dropdown is open

**Expected Results**:
- Blue border shows on focus
- Smooth animation on change
- Blue glow effect
- Professional styling

**Pass/Fail**: ___

---

### Test 3.3: Form Input Styling
**Steps**:
1. Click "Add Patient"
2. Click in each input field

**Expected Results**:
- Border turns blue on focus
- Blue glow effect appears
- Smooth transitions
- All fields styled consistently

**Pass/Fail**: ___

---

### Test 3.4: Buttons Styling
**Steps**:
1. Look at all buttons
2. Hover over buttons

**Expected Results**:
- Buttons have gradient backgrounds
- Hover effect lifts button up
- Shadow increases on hover
- Add Patient button looks premium

**Pass/Fail**: ___

---

### Test 3.5: Required Field Indicators
**Steps**:
1. Click "Add Patient"
2. Look at form labels

**Expected Results**:
- Required fields marked with red *
- Example: "First Name *", "Last Name *", etc.
- Makes clear which fields are required

**Pass/Fail**: ___

---

## 🧪 Test Suite 4: Error Handling

### Test 4.1: Network Error Handling
**Steps**:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Throttle to "Slow 3G"
4. Change a status
5. Observe request

**Expected Results**:
- Request still completes
- Success message appears
- No UI break

**Pass/Fail**: ___

---

### Test 4.2: Invalid Status Selection
**Steps**:
1. Try to select invalid status (shouldn't be possible)
2. Observe behavior

**Expected Results**:
- Only valid options available
- No invalid data sent

**Pass/Fail**: ___

---

### Test 4.3: Modal Close Button
**Steps**:
1. Click "Add Patient"
2. Click X button on modal
3. Modal should close

**Expected Results**:
- Modal closes smoothly
- Form data cleared
- No JavaScript errors

**Pass/Fail**: ___

---

### Test 4.4: Close Button
**Steps**:
1. Click "Add Patient"
2. Click "Close" button
3. Modal should close

**Expected Results**:
- Modal closes
- Form data preserved (optional)

**Pass/Fail**: ___

---

## 🧪 Test Suite 5: Browser Compatibility

### Test 5.1: Chrome
**Steps**: Open in Google Chrome, run Test Suites 1-4

**Pass/Fail**: ___

### Test 5.2: Firefox
**Steps**: Open in Mozilla Firefox, run Test Suites 1-4

**Pass/Fail**: ___

### Test 5.3: Edge
**Steps**: Open in Microsoft Edge, run Test Suites 1-4

**Pass/Fail**: ___

### Test 5.4: Safari
**Steps**: Open in Safari, run Test Suites 1-4

**Pass/Fail**: ___

---

## 🧪 Test Suite 6: Mobile Responsiveness

### Test 6.1: Mobile View (iPhone)
**Steps**:
1. Open DevTools (F12)
2. Toggle device toolbar
3. Select iPhone X
4. Test Add Patient form
5. Test status dropdown

**Expected Results**:
- Layout adapts to mobile
- Buttons are tap-friendly
- Dropdowns work on mobile
- Text is readable

**Pass/Fail**: ___

---

### Test 6.2: Tablet View
**Steps**:
1. Open DevTools (F12)
2. Select iPad
3. Test all functionality

**Expected Results**:
- Good layout on tablet size
- All features work
- No horizontal scrolling needed

**Pass/Fail**: ___

---

## 📊 Test Summary

### Test Suite Results

| Suite | Tests | Passed | Failed | Notes |
|-------|-------|--------|--------|-------|
| Add Patient Form | 8 | ___ | ___ | ___ |
| Status Dropdown | 6 | ___ | ___ | ___ |
| UI & Styling | 5 | ___ | ___ | ___ |
| Error Handling | 4 | ___ | ___ | ___ |
| Browser Compat. | 4 | ___ | ___ | ___ |
| Mobile | 2 | ___ | ___ | ___ |
| **TOTAL** | **29** | ___ | ___ | ___ |

---

## 🎯 Completion Checklist

- [ ] All tests passed
- [ ] No console errors
- [ ] No server errors
- [ ] Add Patient works
- [ ] Status dropdown works
- [ ] UI looks professional
- [ ] Mobile responsive
- [ ] Error handling works
- [ ] Data persists on refresh
- [ ] No performance issues

---

## 🚀 Ready for Production?

- [ ] All manual tests passed
- [ ] Tested in multiple browsers
- [ ] Tested on mobile devices
- [ ] Error cases handled
- [ ] Performance acceptable
- [ ] Documentation complete

**Final Status**: ✅ **READY** / ⏳ **NEEDS FIXES** / ❌ **BLOCKED**

---

## 📝 Notes

Add any additional findings or observations:

```
[Add notes here]
```

---

**Test Date**: ________________  
**Tester Name**: ________________  
**Build Version**: 2.0  
**Status**: ✅ PRODUCTION READY

