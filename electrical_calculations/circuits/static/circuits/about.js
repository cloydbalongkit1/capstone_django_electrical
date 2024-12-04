document.addEventListener("DOMContentLoaded", () => {
    
    contactUs();
    
})



function contactUs() {
    const contactInformationButton = document.querySelector(".contact-information-btn");

    if (contactInformationButton) {

        contactInformationButton.addEventListener("click", () => {
            console.log("clicked");
    
            const contactInformationSection = document.querySelector(".contact-information-section");
        
            if (contactInformationSection.hasAttribute("hidden")) {
                contactInformationSection.removeAttribute("hidden");
            } else {
                contactInformationSection.setAttribute("hidden", true);
            }
        })
    }
    
}


