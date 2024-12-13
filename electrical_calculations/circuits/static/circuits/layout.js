document.addEventListener("DOMContentLoaded", () => {
    queryMessage();
    bellClicked();
    concernEmailClicked();

    
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



function queryMessage() {
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token-meta"]').content;
    const messageSpan = document.querySelector(".user_query_messages_span");

    if (messageSpan) {
        fetch('/query_messages', {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfTokenMeta,
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return response.json();
        })
        .then(data => {
            console.log("Backend Data:", data);

            const badge = messageSpan.querySelector(".badge");
            if (badge && data.unread_count !== undefined) {
                badge.textContent = data.unread_count;
            }
        })

        .catch(error => {
            console.error("Error fetching query messages:", error);
        });
    }
}



function bellClicked() {
    const bell = document.querySelector(".bell-hover");
    if (bell) {
        bell.addEventListener('click', () => {
            window.location.href = '/contacted_messages';
        }) 
    }
}



function concernEmailClicked() {
    const concernEmails = document.querySelectorAll(".concern_email_lists");
    if (concernEmails) {
        concernEmails.forEach((concern) => {
            concern.addEventListener('click', () => {
                const concernID = concern.getAttribute("name");
                window.location.href = `/contacted_message/${encodeURIComponent(concernID)}`;
            })
        })
    }
}

