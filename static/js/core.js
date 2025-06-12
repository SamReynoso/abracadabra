function toggleOrRemoveClass(element, toggleElement, className, event, overlay=null) {
    if (toggleElement.contains(event.target)) {
        element.classList.toggle(className);
        if (overlay) {
            overlay.classList.toggle('active');
        }
    } else if (!element.contains(event.target)) {
        element.classList.remove(className);
        if (overlay) {
            overlay.classList.remove('active');
        }
    } else {
    }
}

function searchAddress(el) {
    const query = el.value.trim();
    const container = el.closest(".form-container");
    const suggestions = container.querySelector(".suggestions");

    if (!query) {
        suggestions.innerHTML = "";
        return;
    }
        

    fetch("/geo/api/?q=" + encodeURIComponent(query) + "&limit=5")
        .then(response => response.json())
        .then(data => {
            suggestions.innerHTML = "";

            data.features.forEach(feature => {
                const item = document.createElement("li");
                item.textContent = feature.properties.name + ", " + (feature.properties.city || "");

                item.addEventListener("click", function () {
                    container.querySelector(".street").value = feature.properties.street|| "";
                    container.querySelector(".city").value = feature.properties.city || "";
                    container.querySelector(".state").value = feature.properties.state || "";
                    container.querySelector(".postal_code").value = feature.properties.postcode || "";
                    container.querySelector(".country").value = feature.properties.country || "";
                    container.querySelector(".lat").value = feature.geometry.coordinates[1];
                    container.querySelector(".lon").value = feature.geometry.coordinates[0];

                    el.value = item.textContent;
                    suggestions.innerHTML = "";
                });

                suggestions.appendChild(item);
            });
        });

    document.query
}

document.body.addEventListener('htmx:configRequest', function (event) {
        event.detail.headers['Cache-Control'] = 'no-cache';
});

function openAppDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById(event.target.dataset.toggle);
    if (dropdown) {
        const openDropdown = document.querySelector('.collapse-navigation-list.open');
        if (openDropdown && openDropdown !== dropdown) {
            console.log("Closing other dropdowns");
            openDropdown.classList.remove('open');
        }
        dropdown.classList.toggle('open');
    } else {
        console.error("Dropdown with ID " + event.target.dataset.toggle + " not found.");
    }
}

window.addEventListener('click', function(event) {
    if (event.target.dataset.toggle) {
        return;
    }
    const openDropdown = document.querySelector('.collapse-navigation-list.open');
    if (openDropdown) {
        openDropdown.classList.remove('open');
    }
});

window.addEventListener('toggle', function(event) {
    const details = event.target;

    if (details.tagName === 'DETAILS' && details.open) {
        const summary = details.querySelector('summary');
        if (summary) {
            summary.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

function handleClose() {
    const openDropdown = document.querySelector('.collapse-navigation-list.open');
    if (openDropdown) {
        openDropdown.classList.remove('open');
    }
    const suggestions = document.querySelector(".suggestions");
    if (suggestions) {
        suggestions.innerHTML = "";
    }
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebar.classList.contains('slide-in')) {
        sidebar.classList.remove('slide-in');
    }
    const mutedOverlay = document.getElementById('mutedOverlay');
    if (mutedOverlay) {
        mutedOverlay.classList.remove('active');
    }
    const navbarDropdown = document.getElementById('navbarDropdown');
    if (navbarDropdown && navbarDropdown.classList.contains('show')) {
        navbarDropdown.classList.remove('show');
    }
    const navbarDropdownArrow = document.getElementById('navbarDropdowArrow');
    if (navbarDropdownArrow && navbarDropdownArrow.classList.contains('rotate')) {
        navbarDropdownArrow.classList.remove('rotate');
    }
}


document.addEventListener("blur", function(event) {
    handleClose();
});

document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        handleClose();
        return;
    }

    const focused = document.activeElement;

    if (focused.id === "addressInput") {
        const suggestions = focused.closest(".form-container").querySelector(".suggestions");
        const activeItem = suggestions.querySelector(".active"); 
        if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            if (activeItem) {
                const nextItem = event.key === "ArrowDown" ? activeItem.nextElementSibling : activeItem.previousElementSibling;
                if (nextItem) {
                    activeItem.classList.remove("active");
                    nextItem.classList.add("active");
                }
            } else {
                if (event.key === "ArrowDown") {
                    const firstItem = suggestions.querySelector("li");
                    if (firstItem) {
                        firstItem.classList.add("active");
                    }
                }
            }
        }
        if (event.key === "Enter") {
            if (activeItem) {
                activeItem.click();
            } else {
                suggestions.innerHTML = "";
            }
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const navbarDropdownToggle = document.getElementById('navbarDropdowToggle');
    const navbarDropdown = document.getElementById('navbarDropdown');
    const mutedOverlay = document.getElementById('mutedOverlay');
    const navbarDropdownArrow = document.getElementById('navbarDropdowArrow');

    document.addEventListener('click', (event) => {
        toggleOrRemoveClass(sidebar, sidebarToggle, 'slide-in', event, mutedOverlay);
        toggleOrRemoveClass(navbarDropdown, navbarDropdownToggle, 'show', event);
        toggleOrRemoveClass(navbarDropdownArrow, navbarDropdownToggle, 'rotate', event);
    });

});
