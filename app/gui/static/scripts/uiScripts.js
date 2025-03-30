var burgerMenu = document.getElementById("burger_menu");
var burgerIcon = document.getElementById("burger_icon");
// Menu Items
var homeMenu = document.getElementById('home');
var projectMenu = document.getElementById("project");
var contactMenu = document.getElementById("contact");

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


