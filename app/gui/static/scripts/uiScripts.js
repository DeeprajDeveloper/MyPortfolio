// Description: This script handles the UI interactions for the web application, including the burger menu and chat dialog functionality.
// Burger Menu
var burgerMenu = document.getElementById("burger_menu");
var burgerIcon = document.getElementById("burger_icon");
var homeMenu = document.getElementById('home');

burgerIcon.addEventListener('click', () => {
    
    if(burgerMenu.style.display === '' || burgerMenu.style.display === 'none') {
        burgerMenu.style.display = 'block';
        burgerIcon.classList.add("burger_icon_clicked");
    } else {
        burgerMenu.style.display = "none";
        burgerIcon.classList.remove("burger_icon_clicked");
    }
});


document.addEventListener('click', (event) => {
    
    if (!burgerMenu.contains(event.target) && !burgerIcon.contains(event.target)) {
        burgerMenu.style.display = "none";
        burgerIcon.classList.remove("burger_icon_clicked");
    }
});

homeMenu.addEventListener("click", () => { homeMenu.classList.add("active_menu_item"); });

// Disable Submit Button after form is populated
function disableSubmit(form) {
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.innerText = "Sending Message...";
}




