// otptimer.js
document.addEventListener("DOMContentLoaded", function() {
    const initialCountdownTime = 180; // 2 minutes in seconds
    const homeUrl = '/'; // Change this to the correct home URL

    // Function to start the countdown
    function startCountdown() {
        let countdownTime = getRemainingTime();

        const countdownInterval = setInterval(function() {
            if (countdownTime <= 0) {
                clearInterval(countdownInterval);
                localStorage.removeItem('countdownTime'); // Clear stored countdown time
                window.location.href = homeUrl; // Redirect to home URL after time exceeds
            } else {
                countdownTime--;
                localStorage.setItem('countdownTime', countdownTime); // Update stored countdown time
                updateCountdownDisplay(countdownTime);
            }
        }, 1000);
    }

    // Function to update the display of the countdown timer
    function updateCountdownDisplay(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        document.getElementById('countdown-timer').textContent = `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }

    // Function to get the remaining time from localStorage or set to initial time
    function getRemainingTime() {
        const storedTime = localStorage.getItem('countdownTime');
        return storedTime !== null ? parseInt(storedTime, 10) : initialCountdownTime;
    }

    startCountdown();
});
