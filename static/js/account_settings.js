// Script pour la page des paramètres du compte

document.addEventListener("DOMContentLoaded", function () {
  // Gestion de l'upload de fichier
  const avatarInput = document.querySelector('input[type="file"]');
  if (avatarInput) {
    avatarInput.addEventListener("change", function () {
      if (this.files && this.files[0]) {
        const fileSize = this.files[0].size / 1024 / 1024; // en MB

        // Vérifier la taille du fichier (max 5MB)
        if (fileSize > 5) {
          alert("La taille du fichier ne doit pas dépasser 5MB.");
          this.value = "";
          return;
        }

        // Prévisualisation de l'image
        const file = this.files[0];
        const fileReader = new FileReader();

        fileReader.onload = function (e) {
          // Chercher l'image ou créer un élément si c'est la première upload
          let avatarPreview = document.querySelector(".flex.items-start.mb-2 img");
          let avatarContainer = document.querySelector(".flex.items-start.mb-2");

          if (avatarPreview) {
            // Mettre à jour l'image existante
            avatarPreview.src = e.target.result;
          } else {
            // Remplacer le div par une image
            const placeholderDiv = document.querySelector(".flex.items-start.mb-2 div.rounded-full");

            if (placeholderDiv && avatarContainer) {
              // Créer une nouvelle image
              const newImage = document.createElement("img");
              newImage.src = e.target.result;
              newImage.alt = "Avatar Preview";
              newImage.className = "w-24 h-24 rounded-full object-cover mr-4";

              // Remplacer le div par l'image
              avatarContainer.replaceChild(newImage, placeholderDiv);
            }
          }
        };

        fileReader.readAsDataURL(file);
      }
    });
  }

  // Animation de notification après sauvegarde réussie
  const showSaveSuccess = () => {
    // Vérifier si un message de succès existe dans la page
    const messages = document.querySelectorAll(".bg-green-100");

    if (messages.length > 0) {
      // Faire défiler vers le haut pour voir le message
      window.scrollTo({ top: 0, behavior: "smooth" });

      // Ajouter une classe d'animation
      messages.forEach((message) => {
        message.classList.add("alert-animation");
      });
    }
  };

  // Exécuter au chargement de la page
  showSaveSuccess();

  // Gestion du formulaire
  const form = document.querySelector(".account-settings-form");
  if (form) {
    form.addEventListener("submit", function () {
      const submitBtn = this.querySelector('button[type="submit"]');

      // Désactiver le bouton et montrer un état de chargement
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Enregistrement...
                `;
      }
    });
  }
});
