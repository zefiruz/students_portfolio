document.addEventListener("DOMContentLoaded", function () {
    const yearElem = document.getElementById("current-year");
    if (yearElem) {
        yearElem.textContent = new Date().getFullYear();
    }
});