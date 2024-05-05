document.addEventListener('DOMContentLoaded', function() {
    // Function to check if the email is in the correct format
    function validateEmail(email) {
      var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }
  
    // Function to check if the password meets the criteria
    function checkPasswordStrength(password) {
      var alphaNumericRegex = /^(?=.*[a-zA-Z])(?=.*[0-9])/;
      return password.length >= 8 && alphaNumericRegex.test(password);
    }
  
    // Function to handle form submission and validate input fields
    function validateResetPasswordForm(event) {
      var emailInput = document.getElementById('email');
      var passwordInput = document.getElementById('password');
      var repasswordInput = document.getElementById('repassword');
  
      var email = emailInput.value;
      var password = passwordInput.value;
      var repassword = repasswordInput.value;
  
      // Check email format
      var emailError = document.getElementById('emailError');
      if (!validateEmail(email)) {
        emailError.textContent = "Please enter a valid email address.";
        event.preventDefault(); // Prevent form submission
        return false;
      } else {
        emailError.textContent = ""; // Clear error message if email is valid
      }
  
      // Check password strength
      var passwordError = document.getElementById('passwordError');
      if (!checkPasswordStrength(password)) {
        passwordError.textContent = "Password should be at least 8 characters long and contain a mix of alphabetic and numeric characters.";
        event.preventDefault(); // Prevent form submission
        return false;
      } else {
        passwordError.textContent = ""; // Clear error message if password is strong
      }
  
      // Check if password and confirm password match
      var repasswordError = document.getElementById('repasswordError');
      if (password !== repassword) {
        repasswordError.textContent = "Passwords do not match.";
        event.preventDefault(); // Prevent form submission
        return false;
      } else {
        repasswordError.textContent = ""; // Clear error message if passwords match
      }
  
      // If all validations pass, allow form submission
      return true;
    }
  
    // Add event listener to form submission
    var resetPasswordForm = document.getElementById('resetPasswordForm');
    if (resetPasswordForm) {
      resetPasswordForm.addEventListener('submit', validateResetPasswordForm);
    }
  });
  