document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth < 576) {
        var abbrElements = document.getElementsByClassName('abbr');
        for (var i = 0; i < abbrElements.length; i++) {
            abbrElements[i].textContent = abbrElements[i].textContent.charAt(0);
        }
    }
});