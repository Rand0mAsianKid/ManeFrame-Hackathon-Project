from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Plant
from . import db
import json
from flask import Flask, request, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        '''if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')'''


        if request.method == 'POST': 
            plant = request.form.get('file')#Gets the file from the HTML 

        if plant is None:
            flash('No File Added!', category='error') 
        else:
            new_plant = Plant(data=plant, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_plant) #adding the note to the database 
            db.session.commit()
            flash('File added!', category='success')

    return render_template("home.html", user=current_user)



def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        
        if file:
            note = request.form.get('note', '')  # Get the note from the form
            filename = secure_filename(file.filename)
            file_data = file.read()  # Read the file data

            new_plant = Plant(note=note, file_name=filename, file_data=file_data, user_id=current_user.id)
            db.session.add(new_plant)
            db.session.commit()

            flash('File added!', category='success')
            return redirect(url_for('views.upload_file'))  # Redirect after POST to avoid form resubmission

    return render_template('upload.html')



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})