document.addEventListener("DOMContentLoaded", function () {
  // Détecte les boutons d'export PDF
  const exportButtons = document.querySelectorAll(".pdf-export-btn");

  exportButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      // Ajouter une animation de chargement
      button.classList.add("animate-pulse");
      button.querySelector("span").textContent = "Génération du PDF...";

      // Réactiver le bouton après 3 secondes (temps moyen de génération)
      setTimeout(() => {
        button.classList.remove("animate-pulse");
        button.querySelector("span").textContent = "Exporter en PDF";
      }, 3000);
    });
  });

  // Fonction pour prévisualiser le PDF avant export (si implémenté)
  window.previewPDF = function (gameId) {
    const modal = document.getElementById("pdf-preview-modal");
    if (modal) {
      modal.classList.remove("hidden");

      // Charger la prévisualisation dans un iframe
      const previewFrame = document.getElementById("pdf-preview-frame");
      if (previewFrame) {
        previewFrame.src = `/generator/game/${gameId}/preview-pdf/`;
      }
    }
  };

  // Fermer la modal de prévisualisation
  const closeModalButtons = document.querySelectorAll(".close-modal-btn");
  closeModalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = document.getElementById("pdf-preview-modal");
      if (modal) {
        modal.classList.add("hidden");
      }
    });
  });
});
