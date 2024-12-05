from flask import Flask, request, jsonify, render_template, send_file, flash
import json
import os
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

def filter(meta, data, gender, fileName, time_filter=None):
    # Filtrage par genre
    gender = gender.lower()
    genderMetaAvailable = meta['Gender'].unique()
    if gender in genderMetaAvailable:
        filtered_meta = meta[meta['Gender'] == gender]
        idVox = np.array(filtered_meta['VoxCeleb1 ID'])
        filtered_data = data[data['speaker_id'].isin(idVox)]
    else:
        return f"gender must be in {genderMetaAvailable} (Capital except)"

    # Filtrage par durée (si time_filter est fourni)
    if time_filter and time_filter != "indifferent":
        # Dictionnaire des tranches de durée
        tranche = {
            'tc': (0, 3),
            'c': (3, 5),
            'm': (5, 8),
            'l': (8, 20),
            'tl': (20, 55)
        }
        
        time_filter = time_filter.lower()  # Convertir en minuscule pour correspondre au dictionnaire
        if time_filter in tranche:
            # Calculer la durée totale de chaque audio pour chaque speaker
            duration = pd.DataFrame(columns=["speaker_id", "time", "timeSlice"])
            for val in filtered_data["speaker_id"].unique():
                time = len(filtered_data[filtered_data['speaker_id'] == val]) / 16  # fs = 16 (échantillonnage)
                if time > 0:
                    if tranche['tc'][0] < time <= tranche['tc'][1]:
                        timeSlice = 'tc'
                    elif tranche['c'][0] < time <= tranche['c'][1]:
                        timeSlice = 'c'
                    elif tranche['m'][0] < time <= tranche['m'][1]:
                        timeSlice = 'm'
                    elif tranche['l'][0] < time <= tranche['l'][1]:
                        timeSlice = 'l'
                    elif time > tranche['tl'][0]:
                        timeSlice = 'tl'
                    else:
                        timeSlice = None
                    
                    # Ajout du speaker_id et de la tranche de temps
                    row = pd.DataFrame({"speaker_id": [val], "time": [time], "timeSlice": [timeSlice]})
                    duration = pd.concat([duration, row], ignore_index=True)
            
            # Filtrer les données par tranche de durée
            filtered_data = filtered_data[filtered_data['speaker_id'].isin(duration[duration["timeSlice"] == time_filter]["speaker_id"])]
        else:
            raise f"time_filter must be in {tranche.keys()} (Capital except)"

    # Sauvegarde du fichier filtré
    filtered_data.to_pickle(fileName)
    return fileName
    
# Chemin vers le fichier JSON des filtres
FILTER_FILE = "filters.json"

def load_filters():
    if os.path.exists(FILTER_FILE):
        with open(FILTER_FILE, "r") as f:
            return json.load(f)
    return []

def save_filters(filters):
    with open(FILTER_FILE, "w") as f:
        json.dump(filters, f, indent=4)

@app.route('/filters', methods=['GET'])
def get_filters():
    filters = load_filters()
    return jsonify(filters)

@app.route('/delete_filter/<filter_name>', methods=['POST'])
def delete_filter(filter_name):
    filters = load_filters()

    updated_filters = [f for f in filters if f["name"].lower() != filter_name.lower()]
    save_filters(updated_filters)
    return jsonify({"message": f"Le filtre '{filter_name}' a été supprimé avec succès."}), 200


# Route pour ajouter un filtre
@app.route('/manage_filters', methods=['GET', 'POST'])
def manage_filter():
    if request.method == 'POST':
        filter_name = request.form.get('filter_name')
        filter_choices = request.form.get('filter_choice')

        if not filter_name or not filter_choices:
            return jsonify({"error": "Le nom du filtre et les choix sont obligatoires."}), 400

        filters = load_filters()

        new_filter = {"name": filter_name, "choices": [choice.strip() for choice in filter_choices.split(",")]}
        filters.append(new_filter)
        save_filters(filters)

        return render_template(
            'add_filter.html', 
            success_message=f"Le filtre '{filter_name}' a été ajouté avec succès.",
            filters=filters
        )

    filters = load_filters()
    return render_template('manage_filters.html', filters=filters)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        meta_file = request.files['meta_file']
        data_file = request.files['data_file']
        gender = request.form['gender']
        time_record = request.form['time_record']
        
        meta = pd.read_csv(meta_file, sep="\t")
        data = pd.read_pickle(data_file)
        
        output_filename = request.form['output_filename']
        result = filter(meta[meta['Set'] == 'test'], data, gender, 'output/'+output_filename, time_filter=time_record)

        if result.endswith('.pkl'):
            return send_file(result, as_attachment=True)
        else:
            flash(f"Error nom du fichier le fichier doit contenir l'extension .pkl: {result}")
    filters = load_filters()
    return render_template('index.html', filters=filters)

if __name__ == '__main__':
    app.run(debug=True)
