/**
 * Système de gestion des onglets
 * Permet de basculer entre différents onglets dans l'interface
 */

function showTab(tabName) {
  console.log("Changement d'onglet vers:", tabName);

  // Cacher tous les contenus d'onglets
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.add("hidden");
  });

  // Réinitialiser tous les boutons d'onglets
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("border-blue-500", "text-blue-600");
    btn.classList.add("border-transparent", "text-gray-500");
  });

  // Afficher le contenu de l'onglet sélectionné
  const contentElement = document.getElementById("content-" + tabName);
  if (contentElement) {
    contentElement.classList.remove("hidden");
    console.log("Contenu affiché:", "content-" + tabName);
  } else {
    console.error("Élément non trouvé:", "content-" + tabName);
  }

  // Mettre en évidence le bouton de l'onglet sélectionné
  const tabElement = document.getElementById("tab-" + tabName);
  if (tabElement) {
    tabElement.classList.remove("border-transparent", "text-gray-500");
    tabElement.classList.add("border-blue-500", "text-blue-600");
  }
}

// Initialisation - s'assurer que le premier onglet est actif au chargement
document.addEventListener("DOMContentLoaded", function () {
  console.log("Initialisation des onglets");

  // Si des onglets sont présents sur la page, activer le premier par défaut
  const tabButtons = document.querySelectorAll(".tab-btn");
  console.log("Onglets trouvés:", tabButtons.length);

  if (tabButtons.length > 0) {
    // Obtenir l'ID du premier onglet à partir de son attribut id
    const firstTabId = tabButtons[0].id.replace("tab-", "");
    console.log("Premier onglet:", firstTabId);
    showTab(firstTabId);
  }
});
