// splash.js
document.addEventListener("DOMContentLoaded", function() {
    // Check if the splash screen has been shown before
    if (!sessionStorage.getItem('splashShown')) {
        // Show the splash screen
        const splashScreen = document.getElementById('splash-screen');
        splashScreen.classList.add('visible');

        // Hide the splash screen after 3 seconds
        setTimeout(function() {
            splashScreen.classList.remove('visible');
            // Mark the splash screen as shown
            sessionStorage.setItem('splashShown', 'true');
        }, 3000);
    }
});
