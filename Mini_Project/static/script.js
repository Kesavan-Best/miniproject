document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const loginFormContainer = document.querySelector('.login-form');
    const registerFormContainer = document.querySelector('.register-form');
    const notification = document.getElementById('notification');

    // Toggle between login and register forms
    showRegisterLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginFormContainer.classList.add('hidden');
        registerFormContainer.classList.remove('hidden');
    });

    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        registerFormContainer.classList.add('hidden');
        loginFormContainer.classList.remove('hidden');
    });

    // Show notification
    function showNotification(message, isSuccess) {
        notification.textContent = message;
        notification.className = 'notification ' + (isSuccess ? 'success' : 'error');
        
        setTimeout(() => {
            notification.className = 'notification';
        }, 3000);
    }

    // Clear error messages
    function clearErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
        });
    }

    // Login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        clearErrors();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        let isValid = true;
        
        // Basic validation
        if (!email) {
            document.getElementById('loginEmailError').textContent = 'Email is required';
            isValid = false;
        }
        
        if (!password) {
            document.getElementById('loginPasswordError').textContent = 'Password is required';
            isValid = false;
        }
        
        if (!isValid) return;
        
        // Send login request
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, true);
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showNotification(data.message, false);
            }
        })
        .catch(error => {
            showNotification('An error occurred. Please try again.', false);
        });
    });

    // Register form submission
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        clearErrors();
        
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('registerConfirmPassword').value;
        
        let isValid = true;
        
        // Basic validation
        if (!username) {
            document.getElementById('registerUsernameError').textContent = 'Username is required';
            isValid = false;
        } else if (username.length < 3) {
            document.getElementById('registerUsernameError').textContent = 'Username must be at least 3 characters';
            isValid = false;
        }
        
        if (!email) {
            document.getElementById('registerEmailError').textContent = 'Email is required';
            isValid = false;
        }
        
        if (!password) {
            document.getElementById('registerPasswordError').textContent = 'Password is required';
            isValid = false;
        } else if (password.length < 6) {
            document.getElementById('registerPasswordError').textContent = 'Password must be at least 6 characters';
            isValid = false;
        }
        
        if (!confirmPassword) {
            document.getElementById('registerConfirmPasswordError').textContent = 'Please confirm your password';
            isValid = false;
        } else if (password !== confirmPassword) {
            document.getElementById('registerConfirmPasswordError').textContent = 'Passwords do not match';
            isValid = false;
        }
        
        if (!isValid) return;
        
        // Send registration request
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                confirm_password: confirmPassword
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, true);
                // Switch to login form after successful registration
                setTimeout(() => {
                    registerFormContainer.classList.add('hidden');
                    loginFormContainer.classList.remove('hidden');
                    registerForm.reset();
                }, 1500);
            } else {
                showNotification(data.message, false);
            }
        })
        .catch(error => {
            showNotification('An error occurred. Please try again.', false);
        });
    });
});