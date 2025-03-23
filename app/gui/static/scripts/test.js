var elemThemeButton = document.getElementById("button_theme");
var elemClassList = elemThemeButton.classList;
var currentCookie = document.cookie;

if (currentCookie === "") {
    console.log("Cookie is blank");
    if (elemClassList.contains("lights_on")) {
        document.cookie = "current_theme=theme-lights-on";
    } else {
        document.cookie = "current_theme=theme-lights-off";
    }
} else {
    console.log("Cookie is not blank");
    var themeValue = currentCookie.split("=")[1];
    switch (themeValue) {
        case 'theme-lights-on':
            console.log('Setting Class theme to ON')
            if(elemClassList.contains('lights_off') === true) { 
                elemClassList.remove('lights_off'); 
                elemClassList.add("lights_on"); 
            }
            else { 
                elemClassList.remove("lights_on"); 
                elemClassList.add("lights_off"); 
            }
            break;
        case 'theme-lights-off':
            console.log("Setting Class theme to OFF");
            if (elemClassList.contains("lights_on") === true) {
                elemClassList.remove("lights_on");
                elemClassList.add("lights_off");
            } else {
                elemClassList.remove("lights_off");
                elemClassList.add("lights_on");
            }
            break;
        default:
            break;
    }
    console.log("Cookie is Set");
}


