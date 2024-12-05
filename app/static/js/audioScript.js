// Sélectionner tous les lecteurs audio

const audioPlayers = document.querySelectorAll('.audio-player');

audioPlayers.forEach((audioPlayer) => {
    const currentTimeCode = audioPlayer.querySelector('.current');
    const durationTime = audioPlayer.querySelector('.total-duration');
    const playBtn = audioPlayer.querySelector('.play-btn');
    const iconPlay = playBtn.querySelector('i');
    const soundBtn = audioPlayer.querySelector('.sound-btn');
    const progressSound = audioPlayer.querySelector('.progress-sound');
    const volumeLvl = audioPlayer.querySelector('.volume-lvl');

    // Charger l'élément audio associé
    const audioElement = new Audio(audioPlayer.dataset.src); // Utiliser une data-attribute pour le fichier audio
    console.log(audioElement);

    // Afficher la durée totale une fois les métadonnées chargées
    audioElement.addEventListener("loadeddata", () => {
        if (audioElement.readyState >= 3) {
            progressSound.setAttribute('value', 0);
            durationTime.textContent = formatTime(audioElement.duration);
        }
    });

    // Gérer la lecture et la pause
    playBtn.addEventListener("click", () => {
        if (audioElement.readyState >= 3) {
            if (audioElement.paused) {
                iconPlay.classList.add('fa-pause');
                iconPlay.classList.remove('fa-play');
                audioElement.play().catch((error) => {
                    console.error("Error trying to play audio:", error);
                });
            } else {
                audioElement.pause();
                iconPlay.classList.remove('fa-pause');
                iconPlay.classList.add('fa-play');
            }
        } else {
            console.log("Audio is not ready yet.");
        }
    });

    // Mettre à jour le temps et la barre de progression
    audioElement.addEventListener('timeupdate', () => {
        const currentTime = audioElement.currentTime;
        const duration = audioElement.duration;
        const progressPercentage = (currentTime / duration) * 100;
        progressSound.setAttribute('value', progressPercentage);
        currentTimeCode.textContent = formatTime(currentTime);
    });

    audioElement.addEventListener('ended', () =>{
        iconPlay.classList.remove('fa-pause');
        iconPlay.classList.add('fa-play');
        audioElement.currentTime = 0;
    })

    // Gérer le contrôle du volume
    volumeLvl.addEventListener('input', (event) => {
        const lvl = event.target.value;
        audioElement.volume = lvl;

        soundBtn.classList.remove('fa-volume-xmark', 'fa-volume-off', 'fa-volume-low', 'fa-volume-high');

        if (lvl == 0) {
            soundBtn.classList.add('fa-volume-xmark');
        } else if (lvl < 0.3) {
            soundBtn.classList.add('fa-volume-off');
        } else if (lvl < 0.6) {
            soundBtn.classList.add('fa-volume-low');
        } else {
            soundBtn.classList.add('fa-volume-high');
        }
    });
});