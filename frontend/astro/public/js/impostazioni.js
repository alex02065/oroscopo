console.log("JS caricato");
document.addEventListener("DOMContentLoaded", function () {
    const btnImpostazioni = document.getElementById("impostazioni");
    const pannello = document.getElementById("pannello-impostazioni");
    const btnChiudi = document.querySelector(".chiudi-impostazioni");

    // Apri il pannello
    btnImpostazioni.addEventListener("click", function () {
        pannello.style.display = "flex";
    });

    // Chiudi il pannello cliccando sulla X
    btnChiudi.addEventListener("click", function () {
        pannello.style.display = "none";
    });

    // Chiudi il pannello cliccando sullo sfondo scuro esterno
    window.addEventListener("click", function (event) {
        if (event.target === pannello) {
            pannello.style.display = "none";
        }
    });
});