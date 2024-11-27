document.addEventListener('DOMContentLoaded', () => {
    
    clickCalculateButton()
    showCalculatedForm()
    
})



function showCalculatedForm() {
    var dataContainer = document.getElementById("show-output-data"); 
    var showOutput = dataContainer.dataset.showOutput; //True and False

    var dataValuesContainer = document.getElementById("output-input-datas");
    var showValues = dataValuesContainer.dataset.showValues; //Values

    var showValuesDict = JSON.parse(showValues);
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


