from flask import Blueprint, flash, render_template, redirect, url_for, request, send_file, jsonify
import pandas as pd
from app.services.filter_service import filters_pkl, load_filters, save_filters
from app.services.filterJoin import filterJoin
from app.services.erreur import InvalidParameter
import os

filters_bp = Blueprint('filters', __name__)

@filters_bp.route('/')
def filters_template():
    return render_template('index.html')

@filters_bp.route('/', methods=['POST'])
def filters_post():
    meta_file = request.files['meta_file']
    data_file = request.files['data_file']
    gender = request.form['gender']
    time_record = request.form['time_record']
    output_filename = request.form['output_filename']
    csv_separator = request.form['csv_separator']

    if meta_file.filename == '':
        flash("Vous devez téléverser un fichier de métadonnées au format CSV.")
    elif data_file.filename == '':
        flash("Vous devez téléverser un fichier de données au format pickle (.pkl).")
    else:
        try:
            meta = pd.read_csv(meta_file, sep=csv_separator)
            data = pd.read_pickle(data_file)
        except pd.errors.EmptyDataError:
            flash("Le fichier de métadonnées est vide ou mal formaté.")
            return redirect(url_for('filters.filters_template'))
        except pd.errors.ParserError:
            flash("Erreur de parsing dans le fichier de métadonnées.")
            return redirect(url_for('filters.filters_template'))
        except Exception as e:
            flash(f"Erreur lors du traitement des fichiers : {e}")
            return redirect(url_for('filters.filters_template'))
        else:
            output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            output_filepath = os.path.join(output_directory, output_filename)

            #result = filters_pkl(meta[meta['Set'] == 'test'], data, gender, output_filepath, time_filter=time_record)
            result = filterJoin(meta[meta['Set'] == 'test'], data, output_filepath, gender, time_record, "/static/wav/")

            if output_filename.endswith('.pkl'):
                return send_file(output_filepath, as_attachment=True)
            else:
                flash(f"Erreur : le nom du fichier de sortie doit contenir l'extension .pkl : {output_filename}")
                return redirect(url_for('filters.filters_template'))

    return redirect(url_for('filters.filters_template'))

    
@filters_bp.route('/list_filters', methods=['GET'])
def get_filters():
    filters = load_filters()
    return jsonify(filters)

# Route pour ajouter un filtre
@filters_bp.route('/manage_filters', methods=['GET', 'POST'])
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

        flash(f"Le filtre '{filter_name}' a été ajouté avec succès.", "success")
        return redirect(url_for('filters.manage_filter'))

    filters = load_filters()
    return render_template('manage_filters.html', filters=filters)

@filters_bp.route('/delete_filter/<filter_name>', methods=['POST'])
def delete_filter(filter_name):
    filters = load_filters()

    updated_filters = [f for f in filters if f["name"].lower() != filter_name.lower()]
    save_filters(updated_filters)

    flash(f"Le filtre '{filter_name}' a été supprimé avec succès.", "success")
    return redirect(url_for('filters.manage_filter'))

