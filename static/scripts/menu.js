document.addEventListener("DOMContentLoaded", function () {
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.js';
    jqueryScript.onload = function () {
        $(document).ready(function () {
            const navbar = $("#navbar");
            const screenWidth = window.screen.width;

            loadFontAwesomeIcons();

            if (screenWidth < 900) {
                const icon = $("<i class='menu-icon fas fa-bars'></i>");
                icon.on("click", function () {
                    navbar.find("a").toggle();
                    icon.toggleClass("fa-bars fa-times");
                });
                navbar.append(icon);
                createMenu();
                navbar.find("a").hide();
            } else {
                createMenu();
            }
        });
    };
    document.head.appendChild(jqueryScript);

    function loadFontAwesomeIcons() {
        const faCssLink = document.createElement('link');
        faCssLink.rel = 'stylesheet';
        faCssLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';
        document.head.appendChild(faCssLink);
    }

    function createMenu() {
        const navbar = $("#navbar");
    
        const navItems = [
            { text: "Home", link: "/dashboard", icon: "fas fa-home" },
            { text: "Appointments", link: "#Appointments", icon: "fas fa-calendar-check" },
            { text: "Patients", link: "#Patients", icon: "fas fa-hospital-user" },
            { text: "Observation", link: "#Observation", icon: "fas fa-clipboard" },
            { text: "Account", link: "/account", icon: "fas fa-user" },
            { text: "", link: "/logout", icon: "fas fa-right-from-bracket" },
        ];
    
        $.each(navItems, function (index, item) {
            const link = $("<a></a>");
            link.attr("href", item.link);
    
            const icon = $("<i></i>");
            icon.addClass("fas");
            icon.addClass(item.icon);

            link.append(icon);
            link.append(item.text);
            navbar.append(link);
        });
    }    
});
