document.addEventListener('DOMContentLoaded', () => {

    viewPreviousCalculations();
    prevCalcClassClick();
    profileView();
    deleteButtonPrevPost();

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



function prevCalcClassClick() {
    const previousCalcDiv = document.querySelectorAll(".prev_calc_class");

    if (previousCalcDiv) {
        previousCalcDiv.forEach(item => {
            item.addEventListener('click', () => {
                // const name = item.getAttribute('name');
                const calculated = item.getAttribute("data_calculation_img");
                const calculationResult = document.getElementById("calculation-result");

                calculationResult.innerHTML = `<h3 class="mt-4">Output</h3><img src="data:image/png;base64,${calculated}" alt="Diagram Image">`;
                calculationResult.classList.remove("hidden");

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


function deleteButtonPrevPost() {
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token-meta"]').content;

    const deleteButtonPrevPost = document.querySelectorAll(".deleteButtonPrevPost");
    deleteButtonPrevPost.forEach((delBtn) => {    
        const delBtnId = delBtn.getAttribute('data-post-id-delete');
        delBtn.addEventListener('click', (event) => {
            event.preventDefault();

            fetch(`/delete_previous_calc/${delBtnId}`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfTokenMeta,
                },
            })
            .then(reponse => reponse.json())
            .then(data => {
                
                if (data.message) {
                    alert(data.message); 
                    delBtn.closest('li').remove();

                } else if (data.error) {
                    alert(data.error);  
                }

            })
            .catch(error => {
                console.error(error);
                alert("An error occurred while deleting!");
            })
            
        })
    })
    
}
