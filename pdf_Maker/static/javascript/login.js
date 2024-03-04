document.addEventListener('DOMContentLoaded', function () {
    const flipCheckbox = document.getElementById('flip');
    const loginForm = document.querySelector('.login-form');
    const signupForm = document.querySelector('.signup-form');

    flipCheckbox.addEventListener('change', function () {
        loginForm.classList.toggle('active');
        signupForm.classList.toggle('active');
    });
});