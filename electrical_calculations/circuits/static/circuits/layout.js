document.addEventListener("DOMContentLoaded", () => {
    
    document.getElementById("currentYear").textContent = new Date().getFullYear();
    
    function updateClock() {
        const now = new Date();
        const timeFormatter = new Intl.DateTimeFormat('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true,
        });
        
        const timeString = timeFormatter.format(now);
        document.getElementById("clock").textContent = timeString;
    }

    setInterval(updateClock, 1);
})


