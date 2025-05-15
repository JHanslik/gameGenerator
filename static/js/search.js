/**
 * Gestion de la barre de recherche et des filtres pour les jeux
 */
document.addEventListener("DOMContentLoaded", function () {
  // Récupération des éléments du DOM
  const searchInput = document.getElementById("search-input");
  const genreFilter = document.getElementById("genre-filter");
  const ambianceFilter = document.getElementById("ambiance-filter");
  const searchForm = document.getElementById("search-form");
  const gamesContainer = document.querySelector(".grid");
  const emptyMessage = document.querySelector(".bg-gray-100.rounded-lg");

  // Fonction pour soumettre le formulaire après un délai (debounce)
  let searchTimeout;

  function applySearchDebounce() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      // Pour une meilleure expérience utilisateur, soumettons simplement le formulaire
      // au lieu d'utiliser AJAX, ce qui maintiendra le style d'affichage cohérent
      searchForm.submit();
    }, 500); // Délai de 500ms avant soumission
  }

  // Fonction pour récupérer les jeux via AJAX
  function fetchGamesAjax() {
    // Construire l'URL avec les paramètres de recherche
    const searchParams = new URLSearchParams();
    const searchValue = searchInput ? searchInput.value : "";
    const genreValue = genreFilter ? genreFilter.value : "";
    const ambianceValue = ambianceFilter ? ambianceFilter.value : "";

    if (searchValue) searchParams.append("search", searchValue);
    if (genreValue) searchParams.append("genre", genreValue);
    if (ambianceValue) searchParams.append("ambiance", ambianceValue);

    // Mettre à jour l'URL du navigateur
    updateURLParams("search", searchValue);
    updateURLParams("genre", genreValue);
    updateURLParams("ambiance", ambianceValue);

    // Effectuer la requête AJAX
    fetch(`/games/search-ajax/?${searchParams.toString()}`)
      .then((response) => response.json())
      .then((data) => {
        updateGamesList(data.games);
      })
      .catch((error) => {
        console.error("Erreur lors de la recherche:", error);
      });
  }

  // Fonction pour mettre à jour la liste des jeux
  function updateGamesList(games) {
    if (!gamesContainer) return;

    // Vider le conteneur
    gamesContainer.innerHTML = "";

    // Si aucun jeu n'est trouvé, afficher le message
    if (games.length === 0) {
      if (emptyMessage) emptyMessage.style.display = "block";
      return;
    }

    // Cacher le message si des jeux sont trouvés
    if (emptyMessage) emptyMessage.style.display = "none";

    // Ajouter chaque jeu au conteneur
    games.forEach((game) => {
      const gameCard = document.createElement("div");
      gameCard.className = "bg-white rounded-lg shadow hover:shadow-md transition overflow-hidden";

      // Image ou dégradé par défaut
      let imageHtml = "";
      if (game.image_url) {
        imageHtml = `<img src="${game.image_url}" alt="${game.title}" class="w-full object-cover" />`;
      } else {
        imageHtml = `
        <div class="w-full h-48 bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
            <span class="text-xl font-bold text-white">${game.title}</span>
        </div>
        `;
      }

      // Construction du HTML du jeu
      gameCard.innerHTML = `
          ${imageHtml}
          <div class="p-4">
              <h3 class="font-bold text-lg">${game.title}</h3>
              <div class="flex space-x-2 mb-2">
                  <span class="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">${game.genre}</span>
                  <span class="inline-block px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">${game.ambiance}</span>
              </div>
              <p class="text-gray-700 mb-4 line-clamp-3">${game.description}</p>
              <div class="flex justify-between items-center">
                  <div class="text-xs text-gray-500">
                      <span>Par ${game.creator}</span>
                      <span>• ${game.created_at}</span>
                  </div>
                  <a href="/games/${game.slug}/" class="text-blue-600 hover:underline text-sm">Voir détails</a>
              </div>
          </div>
      `;

      // Ajouter la carte au conteneur
      gamesContainer.appendChild(gameCard);
    });
  }

  // Écouteurs d'événements pour les filtres par select
  if (genreFilter) {
    genreFilter.addEventListener("change", function () {
      searchForm.submit();
    });
  }

  if (ambianceFilter) {
    ambianceFilter.addEventListener("change", function () {
      searchForm.submit();
    });
  }

  // Écouteur d'événement pour la barre de recherche (avec debounce)
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      applySearchDebounce();
    });

    // Gestion de la touche Entrée pour soumettre immédiatement
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        clearTimeout(searchTimeout);
        searchForm.submit();
      }
    });
  }

  // Intercepter la soumission du formulaire pour assurer un comportement cohérent
  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      // Laisser le formulaire se soumettre normalement
    });
  }

  // Mise à jour de l'URL sans recharger la page (pour la navigation historique)
  function updateURLParams(key, value) {
    const url = new URL(window.location.href);
    if (value) {
      url.searchParams.set(key, value);
    } else {
      url.searchParams.delete(key);
    }
    history.pushState({}, "", url);
  }
});
