/*
fonction qui permet de transformer un csv en un tableau HTML
Use case : previsualisation d'un csv
*/

function csvToTable(csv, delimiter = ',', maxRows = 10, containerIdTable = "csv-preview") {
    const rows = csv.trim().split('\n'); // Diviser le contenu du CSV en lignes

    const headers = rows.shift().split(delimiter);

    const numRows = rows.length - 1;
    const numColumns = rows[0].split(delimiter).length;

    const table = document.createElement('table');
    table.classList.add('is-hoverable', 'table');
    table.className = 'table is-bordered is-striped is-narrow is-hoverable is-fullwidth';

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header.trim(); // ajout des entêtes
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    const displayRows = rows.slice(0, maxRows);
    displayRows.forEach(row => {
        const dataRow = document.createElement('tr');
        const cells = row.split(delimiter);
        cells.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell.trim();
            dataRow.appendChild(td);
        });
        tbody.appendChild(dataRow);
    });
    table.appendChild(tbody);

    const previewContainer = document.getElementById(containerIdTable);
    previewContainer.innerHTML = '';
    previewContainer.classList.remove('hidden');
    previewContainer.appendChild(table); // ajout du tableau dans le container

    const csvDimension = document.getElementById('csv-info');
    csvDimension.classList.remove('hidden');
    csvDimension.textContent = `Le fichier contient ${numRows} lignes et ${numColumns} colonnes.`;
}