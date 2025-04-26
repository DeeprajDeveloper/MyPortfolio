var burgerMenu = document.getElementById("burger_menu");
var burgerIcon = document.getElementById("burger_icon");
// Menu Items
var homeMenu = document.getElementById('home');
var projectMenu = document.getElementById("project");
var contactMenu = document.getElementById("contact");

burgerIcon.addEventListener('click', () => {
    if(burgerMenu.style.display === '' || burgerMenu.style.display === 'none') {
        burgerMenu.style.display = 'block';
    } else {
        burgerMenu.style.display = "none";
    }
});

homeMenu.addEventListener("click", () => { homeMenu.classList.add("active_menu_item"); });


const dialog = document.getElementById("dialog");
const showButton = document.getElementById("dialog_show_button");
const closeButton = document.getElementById("dialog_close_button");

// "Show the dialog" button opens the dialog modally
showButton.addEventListener("click", () => { 
    dialog.showModal(); 
    document.body.style.overflow = "hidden";
});

// "Close" button closes the dialog
closeButton.addEventListener("click", () => { 
    dialog.close(); 
    document.body.style.overflow = "";
});
