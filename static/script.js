document.addEventListener("DOMContentLoaded", function () {
    const flashes = document.querySelectorAll(".flash");

    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = "0";

            setTimeout(function () {
                flash.remove();
            }, 300); // Wait for fade-out
        }, 3000); // 3 seconds
    });
});
