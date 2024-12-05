document.addEventListener('DOMContentLoaded', () => {

    clickCalculateButton();
    showCalculatedForm();
    saveCalculations();
    
})



function clearMessage() {
    const alertContainer = document.getElementById("alert-container");
    alertContainer.innerHTML = '';
}



function saveCalculations() {
    const saveButton = document.getElementById("save_calculation_button");
    if (!saveButton) {
        return;
    }
    
    saveButton.addEventListener('click', (event) => {
        event.preventDefault();
        clearMessage()

        const calculateFrom = document.querySelectorAll(".calculate_form");
        const csrfTokenMeta = document.querySelector('meta[name="csrf-token-meta"]');

        let selectedForm;
        let classNameTarget

        calculateFrom.forEach((form) => {
            const parentDiv = form.closest('div');
            if (!parentDiv.hasAttribute('hidden') && window.getComputedStyle(parentDiv).display !== 'none') {   //recommended as && not ||
                selectedForm = parentDiv;
                classNameTarget = parentDiv.classList[0];                
            }
        })

        if (selectedForm) {
            const inputs = selectedForm.querySelectorAll('input');
            const inputValues = {};
            
            inputs.forEach((input) => {
                inputValues[input.name] = input.value;
            })

            if (csrfTokenMeta) {
                const csrfToken = csrfTokenMeta.content;
                const elementImg = document.querySelector('div[data-diagram-img]');
                const imgBase64 = elementImg.getAttribute('data-diagram-img');

                fetch('/save_calc', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        body: inputValues, 
                        name: classNameTarget,
                        imgBase64: imgBase64
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        const alertContainer = document.getElementById("alert-container");
                        alertContainer.innerHTML = `<div class="alert alert-success"><small>${data.message}</small></div>`;
                    } else {
                        const alertContainer = document.getElementById("alert-container");
                        alertContainer.innerHTML = `<div class="alert alert-danger"><small>${data.message}</small></div>`;
                    }
                })
                .catch(error => {
                    const alertContainer = document.getElementById("alert-container");
                    alertContainer.innerHTML = `<div class="alert alert-danger"><small>There was an error with the request.</small></div>`;
                });

            }
            
        }
        
    })
}



function showCalculatedForm() {
    var dataContainer = document.getElementById("show-output-data"); 
    if (!dataContainer) {
        return; 
    }

    var showOutput = dataContainer.dataset.showOutput; //True and False
    
    var dataValuesContainer = document.getElementById("output-input-datas");
    if (!dataValuesContainer) {
        return; 
    }

    var showValues = dataValuesContainer.dataset.showValues; //Values from the input
    var showValuesDict = JSON.parse(showValues); // parase to json to access

    try {

        if (showValuesDict.name === "power_triangle") {
            var P = showValuesDict.P; 
            var Q = showValuesDict.Q; 
            var S = showValuesDict.S; 
            var pf = showValuesDict.pf;

            var pInput = document.querySelector('input[name="power_triangle_P"]');
            var qInput = document.querySelector('input[name="power_triangle_Q"]');
            var sInput = document.querySelector('input[name="power_triangle_S"]');
            var pfInput = document.querySelector('input[name="power_triangle_pf"]');
        
            if (showOutput){
                document.querySelector(".power_triangle").removeAttribute("hidden");
                pInput.value = P;
                qInput.value = Q;
                sInput.value = S;
                pfInput.value = pf;
            }
        }

        if (showValuesDict.name === "phasor_diagram") {

            var V1_magnitude = showValuesDict.V1_magnitude;
            var V1_angle = showValuesDict.V1_angle
            var V2_magnitude = showValuesDict.V2_magnitude;
            var V2_angle = showValuesDict.V2_angle
            var V3_magnitude = showValuesDict.V3_magnitude;
            var V3_angle = showValuesDict.V3_angle

            var V1_magnitude_input = document.querySelector('input[name="V1_magnitude"]');
            var V1_angle_input = document.querySelector('input[name="V1_angle"]');
            var V2_magnitude_input = document.querySelector('input[name="V2_magnitude"]');
            var V2_angle_input = document.querySelector('input[name="V2_angle"]');
            var V3_magnitude_input = document.querySelector('input[name="V3_magnitude"]');
            var V3_angle_input = document.querySelector('input[name="V3_angle"]');
            

            if (showOutput){
                document.querySelector(".phasor").removeAttribute("hidden");
                V1_magnitude_input.value = V1_magnitude
                V1_angle_input.value = V1_angle
                V2_magnitude_input.value = V2_magnitude
                V2_angle_input.value = V2_angle
                V3_magnitude_input.value = V3_magnitude
                V3_angle_input.value = V3_angle                
            }
        }
    
    } catch (error) {
        console.error("Failed to parse or use 'showValues: ", error);
        
    }
    
}



function clickCalculateButton() {
    document.querySelectorAll('.calc_btn').forEach(button => {
        button.addEventListener('click', () => {

            let data = button.dataset.function;
            document.querySelectorAll('.col-md-9 > div').forEach(div => { 
                    div.hidden = true; 
                });

            let selected = document.querySelector(`.${data}`)
            if (selected) {
                selected.hidden = false;
            } else {
                console.error(`No form found for class: ${data}`);
            }
        })
    })
}


