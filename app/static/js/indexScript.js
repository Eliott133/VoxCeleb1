const inputCsv = document.getElementById("file_csv_input");
const delimiterSelect = document.getElementById('csv_separator');
const maxRow = document.getElementById('preview_head_number');
const inputFileNameOutput = document.getElementById('output_filename');
const filtersInput = document.querySelectorAll('.filter_input');
const dateTime = new Date();
var delimiterSelected = '\t';
var maxRowSelected = 10
let activeFilters = {};

delimiterSelect.addEventListener('change', ()=>{
    delimiterSelected = delimiterSelect.value;
})

maxRow.addEventListener('change', ()=>{
    maxRowSelected = maxRow.value;
})

filtersInput.forEach((element) => {
    activeFilters[element.id] = element.options[element.selectedIndex].dataset.filterName || 'default';
});

let filterString = Object.entries(activeFilters)
        .map(([key, value]) => key+"_"+value).join('_');

let fileOutputName = filterString+"_"+formatDateTime(dateTime)+".pkl";
inputFileNameOutput.value = fileOutputName;

filtersInput.forEach((element) => {
    element.addEventListener('change', () => {
        activeFilters[element.id] = element.options[element.selectedIndex].dataset.filterName;
        const filterString = Object.entries(activeFilters)
            .map(([key, value]) => key+"_"+value).join('_');
        fileOutputName = filterString+"_"+formatDateTime(dateTime)+".pkl";
        inputFileNameOutput.value = fileOutputName;
    })
});

inputCsv.addEventListener("change", (event) => {
    file = event.target.files[0];
    if (file && file.name.endsWith('.csv')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const csvData = e.target.result; // Contenu du fichier CSV
            csvToTable(csvData, delimiterSelected, maxRowSelected)
        };
        reader.readAsText(file);
    } else {
        console.warn('Veuillez sélectionner un fichier CSV.');
    }
});