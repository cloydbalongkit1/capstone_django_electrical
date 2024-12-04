document.addEventListener('DOMContentLoaded', () => {

    viewPreviousCalculations();
    dataPowerTriangleClick();
    profileView();

})



function profileView() {
    const profileButton = document.querySelector(".home_view_profile_btn")

    if (profileButton) {
        profileButton.addEventListener('click', () => {
            console.log("clicked");
            window.location.href = "/profile_view";
        })
    }
    
}



function dataPowerTriangleClick() {
    const dataPowerTriangleDiv = document.querySelectorAll(".prev_calc_class");

    // no phasor ----> add phasor
    if (dataPowerTriangleDiv) {
        dataPowerTriangleDiv.forEach(item => {            
            item.addEventListener('click', () => {

                console.log(item.getAttribute('name')); // checking what is the clicked item by attribute (name)
                // conditional and to be continue

                const P = item.getAttribute("data-power-triangle-p");
                const Q = item.getAttribute("data-power-triangle-q");
                const S = item.getAttribute("data-power-triangle-s");
                const pf = item.getAttribute("data-power-triangle-pf");

                const formData = new FormData();
                formData.append('power_triangle_P', P);
                formData.append('power_triangle_Q', Q);
                formData.append('power_triangle_S', S);
                formData.append('power_triangle_pf', pf);

                fetch("/power_triangle", {
                    method: "POST",
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token-meta"]').getAttribute('content'),
                        'fromJS': 'fromJS',
                    }
                })
                .then(response => response.text())  // Get the HTML response
                .then(html => {             
                    document.getElementById('calculation-result').innerHTML = html;
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("There was an error processing the request.");
                });
            });
        });
    }
}



function viewPreviousCalculations() {
    const viewPrevCalcBtn = document.querySelector(".home_view_calc_btn")

    if (viewPrevCalcBtn) {
        viewPrevCalcBtn.addEventListener("click", () => {
            window.location.href = "/user_calculations";
        })
    }
}

