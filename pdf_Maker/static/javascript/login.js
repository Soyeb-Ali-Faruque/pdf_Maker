document.addEventListener('DOMContentLoaded', function () {
    const flipCheckbox = document.getElementById('flip');
    const loginForm = document.querySelector('.login-form');
    const signupForm = document.querySelector('.signup-form');

    flipCheckbox.addEventListener('change', function () {
        loginForm.classList.toggle('active');
        signupForm.classList.toggle('active');
    });
});












//---------------------------sign up -------------------------//
document.addEventListener('DOMContentLoaded', function() {
    // Function to check if the email is in the correct format
    function validateEmail(email) {
      var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }
  
    // Function to check if the name contains only alphabets and spaces
    function validateName(name) {
      var nameRegex = /^[A-Za-z\s]+$/;
      return nameRegex.test(name);
    }
  
    // Function to check if the password meets the criteria
    function checkPasswordStrength(password) {
      var alphaNumericRegex = /^(?=.*[a-zA-Z])(?=.*[0-9])/;
      return password.length >= 8 && alphaNumericRegex.test(password);
    }
  
    // Function to handle form submission and validate input fields
    function validateSignupForm(event) {
      var emailInput = document.querySelector('input[name="uemail"]');
      var nameInput = document.querySelector('input[name="uname"]');
      var passwordInput = document.querySelector('input[name="upass"]');
  
      var email = emailInput.value;
      var name = nameInput.value;
      var password = passwordInput.value;
  
      // Check email format
      if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        event.preventDefault(); // Prevent form submission
        return false;
      }
  
      // Check name format
      if (!validateName(name)) {
        alert("Name should only contain alphabets and spaces.");
        event.preventDefault(); // Prevent form submission
        return false;
      }
  
      // Check password strength
      if (!checkPasswordStrength(password)) {
        alert("Password should be at least 8 characters long and contain a mix of alphabetic and numeric characters.");
        event.preventDefault(); // Prevent form submission
        return false;
      }
  
      // If all validations pass, allow form submission
      return true;
    }
  
    // Add event listener to form submission
    var signupForm = document.querySelector('.signup-form form');
    if (signupForm) {
      signupForm.addEventListener('submit', validateSignupForm);
    }
  });
  