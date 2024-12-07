import getFileExtension from './file.js'


const dropZones = document.querySelectorAll('.drop-zone');
const inputFilePkl = document.getElementById('input_file_pkl');
const fileName = document.getElementsByClassName('file-name-indication')[0]
const modalInformation = document.getElementById('modal-warning-file-extension');

dropZones.forEach((dropZone) => {
    const message = dropZone.getElementsByClassName('indication-process-file')[0];

    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        console.log("drag");
        dropZone.classList.add('active-drop-zone');
        
        if (message) {
            message.innerHTML = "Lacher votre fichier";
        }
    });

    dropZone.addEventListener('dragenter', (event) => {
        event.preventDefault();
        console.log("enter");
    });

    dropZone.addEventListener('dragleave', (event) => {
        event.preventDefault();
        dropZone.classList.remove('active-drop-zone');
        
        if (message) {
            message.innerHTML = "Cliquer ou glisser déposer pour télécharger votre fichier de données";
        }
    });

    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();

        const file = event.dataTransfer.files[0];

        if (file) {
            console.log("Fichier déposé : ", file);
            if(getFileExtension(file) != inputFilePkl.getAttribute("accept")){
                dropZone.classList.add('incorrect');
                openModal(modalInformation);

            }else{
                dropZone.classList.remove('incorrect');
                closeModal(modalInformation);
            }
            inputFilePkl.files = event.dataTransfer.files;
            fileName.innerHTML = file.name;
            message.innerHTML = "";
        }
        dropZone.classList.remove('active-drop-zone');
    });


    // REFACTOR : Horrible
    dropZone.querySelectorAll('input[type="file"]')[0].addEventListener('change', (event) => {
        fileName.innerHTML = event.target.files[0].name;
        message.innerHTML = "";
        dropZone.classList.remove('incorrect');
    });
});

(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach((close) => {
    const target = close.closest('.modal');

    close.addEventListener('click', () => {
      closeModal(target);
    });
});

function openModal(modal){
    modal.classList.add('is-active');
}

function closeModal(modal){
    modal.classList.remove('is-active');
}

