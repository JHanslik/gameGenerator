/**
 * Animation de génération de contenu de jeu
 * Gère les animations, particules et suggestions pendant le processus de génération
 */

// Rendre les fonctions accessibles globalement pour la page d'accueil
let showNewSuggestion;
let initParticles;
let initDanceVideo;

document.addEventListener("DOMContentLoaded", function () {
  // Récupération des éléments du DOM
  const checkbox = document.getElementById("with_images");
  const generateBtn = document.getElementById("generate-btn");
  const overlay = document.getElementById("generation-overlay");
  const creativeSuggestionElement = document.getElementById("creative-suggestion");

  // Masquer la barre de progression s'il y en a une
  const progressBar = document.querySelector(".progress-bar");
  if (progressBar) {
    progressBar.style.display = "none";
  }

  // Initialiser les variables pour la génération
  let withImages = checkbox?.checked ? "true" : "false";

  if (checkbox) {
    checkbox.addEventListener("change", function () {
      withImages = this.checked ? "true" : "false";
    });
  }

  // Fonction pour initialiser la fonctionnalité de vidéo de danse (disponible globalement)
  initDanceVideo = function () {
    console.log("Initialisation de la vidéo de danse");
    // On utilise setTimeout pour s'assurer que tous les éléments sont bien chargés
    setTimeout(() => {
      const danceButton = document.getElementById("dance-video-button");
      const videoContainer = document.getElementById("video-container");
      const youtubeIframe = document.getElementById("youtube-iframe");
      const closeVideoBtn = document.getElementById("close-video");

      console.log("Éléments de danse:", { danceButton, videoContainer, youtubeIframe, closeVideoBtn });

      if (danceButton && videoContainer && youtubeIframe) {
        // Vérifier si l'événement est déjà attaché
        if (!danceButton.hasAttribute("data-initialized")) {
          danceButton.setAttribute("data-initialized", "true");

          // Animation légère du bouton pour attirer l'attention
          const animationInterval = setInterval(() => {
            if (danceButton.querySelector("span")) {
              danceButton.querySelector("span").innerHTML =
                danceButton.querySelector("span").innerHTML === "Voulez-vous danser en attendant ? 💃🕺"
                  ? "Cliquez pour vous amuser en attendant ! 🎵🎶"
                  : "Voulez-vous danser en attendant ? 💃🕺";
            } else {
              clearInterval(animationInterval);
            }
          }, 3000);

          // Afficher la vidéo quand on clique sur le bouton
          danceButton.addEventListener("click", function (e) {
            console.log("Bouton de danse cliqué");
            e.preventDefault();

            const danceLink = document.getElementById("dance-link");
            if (danceLink) {
              // Cacher le bouton
              danceLink.style.display = "none";

              // Charger et afficher la vidéo
              youtubeIframe.src = "https://www.youtube.com/embed/m4GbBEEyYtQ?autoplay=1";
              videoContainer.classList.remove("hidden");
            }
          });

          // Fermer la vidéo
          if (closeVideoBtn) {
            closeVideoBtn.addEventListener("click", function () {
              console.log("Bouton de fermeture cliqué");
              youtubeIframe.src = "";
              videoContainer.classList.add("hidden");

              const danceLink = document.getElementById("dance-link");
              if (danceLink) {
                danceLink.style.display = "block";
              }
            });
          }
        }
      }
    }, 100); // Petit délai pour s'assurer que le DOM est prêt
  };

  // Fonction pour initialiser les particules (disponible globalement)
  initParticles = function (container) {
    if (!container) return;

    const particleCount = 30; // Nombre de particules
    for (let i = 0; i < particleCount; i++) {
      createParticle(container);
    }
  };

  function createParticle(container) {
    const particle = document.createElement("div");
    particle.classList.add("particle");

    // Position aléatoire
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;

    // Taille aléatoire
    const size = Math.random() * 6 + 2;

    // Durée aléatoire
    const duration = Math.random() * 3 + 2;

    // Direction aléatoire
    const translateX = (Math.random() - 0.5) * 100;

    // Couleur aléatoire
    const colors = ["#38bdf8", "#60a5fa", "#a5f3fc", "#7dd3fc", "#e0f2fe"];
    const color = colors[Math.floor(Math.random() * colors.length)];

    // Appliquer les styles
    particle.style.left = `${posX}%`;
    particle.style.top = `${posY}%`;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.background = color;
    particle.style.animationDuration = `${duration}s`;
    particle.style.setProperty("--translateX", `${translateX}px`);

    container.appendChild(particle);

    // Relancer la particule après son animation
    setTimeout(() => {
      particle.remove();
      createParticle(container);
    }, duration * 1000);
  }

  // Liste de suggestions créatives à afficher pendant la génération
  const creativeSuggestions = [
    "Pensez à intégrer un arc narratif inattendu dans votre histoire...",
    "Un bon antagoniste a souvent des motivations compréhensibles...",
    "Les meilleurs jeux combinent familiarité et innovation...",
    "Considérez comment l'environnement influence le gameplay...",
    "Un système de progression bien pensé garde les joueurs engagés...",
    "Les personnages mémorables ont souvent des faiblesses marquées...",
    "Le worldbuilding se fait par petites touches, pas seulement par exposition...",
    "Pensez aux émotions que vous souhaitez provoquer chez le joueur...",
    "Un bon level design guide subtilement le joueur sans qu'il s'en aperçoive...",
    "La musique et l'ambiance sonore sont essentielles à l'immersion...",
    "L'équilibre entre défi et récompense est crucial pour l'expérience de jeu...",
    "Les meilleurs jeux permettent plusieurs façons d'atteindre un objectif...",
    "Le rythme du jeu devrait alterner entre tension et détente...",
    "N'oubliez pas que les mécaniques de jeu doivent servir l'histoire, et inversement...",
    "Les petits détails environnementaux enrichissent considérablement l'univers...",
    "Un système de combat satisfaisant est souvent simple à comprendre mais difficile à maîtriser...",
  ];

  // Fonction pour afficher une nouvelle suggestion créative (disponible globalement)
  showNewSuggestion = function () {
    if (!creativeSuggestionElement) return;

    creativeSuggestionElement.style.opacity = 0;

    setTimeout(function () {
      const suggestionIndex = Math.floor(Math.random() * creativeSuggestions.length);
      creativeSuggestionElement.textContent = creativeSuggestions[suggestionIndex];
      creativeSuggestionElement.style.opacity = 1;
    }, 500);
  };

  // Initialiser les particules pour n'importe quelle page contenant un overlay
  const particlesContainer = document.querySelector(".particles-container");
  if (particlesContainer) {
    initParticles(particlesContainer);
  }

  // N'initialisons pas automatiquement la vidéo ici, les templates s'en chargeront explicitement
  // initDanceVideo();

  // Page de détail du jeu uniquement - si le bouton de génération existe
  if (generateBtn && overlay) {
    // Ajouter l'événement au bouton
    generateBtn.addEventListener("click", function () {
      // Activer l'overlay
      overlay.classList.add("active");

      const generationMessage = document.getElementById("generation-message");
      const generationStatus = document.getElementById("generation-status");

      // Définir un message simple
      if (generationMessage) {
        generationMessage.textContent = "Génération de l'univers de jeu en cours...";
      }

      if (generationStatus) {
        generationStatus.textContent = "Merci de patienter quelques instants";
      }

      // Initialiser la fonctionnalité de vidéo de danse
      initDanceVideo();

      // Démarrer les suggestions créatives
      showNewSuggestion();
      const suggestionInterval = setInterval(showNewSuggestion, 5000);

      // Simuler un délai avant la redirection
      setTimeout(function () {
        // Obtenir l'ID du jeu à partir des attributs data
        const gameId = overlay.dataset.gameId || (window.location.pathname.match(/\/games\/([^\/]+)\//) || [])[1];

        // Redirection après un délai
        const redirectUrl = `/generator/game/${gameId}/generate/?with_images=${withImages}`;
        window.location.href = redirectUrl;
      }, 3000); // 3 secondes de délai pour voir l'animation
    });
  }
});
