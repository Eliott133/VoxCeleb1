from flask import Blueprint, flash, render_template, redirect, url_for, request, send_file, jsonify
import pandas as pd
from app.services.pkl_service import get_path_audio

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/audio')
def audioListening():
    return render_template('audio.html')

@audio_bp.route('/audio', methods=['post'])
def get_audio():
    file = request.files['pkl_file']
    limit_audio = request.form['limit_audio']
    file_name = file.filename

    if file.filename != '' and allowed_file(file.filename) == 'pkl':
        
        df = pd.read_pickle(file)

        num_lines = len(df)

        tab_path = get_path_audio(df, int(limit_audio))
        
        return render_template('audio.html', src_audio=tab_path, file_name=file_name, num_lines=num_lines, audio_display=limit_audio)
    
    flash("Vous devez téléverser un fichier de données au format .pkl")
    return redirect(url_for('audio.audioListening'))

def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower())
    return filename.rsplit('.', 1)[1].lower()
