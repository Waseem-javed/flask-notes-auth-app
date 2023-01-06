from flask import Blueprint,render_template,flash,request,redirect,url_for
from flask_login import login_required,current_user

from . import db
from .models import Note


views = Blueprint('views',__name__)


@views.route('/', methods=['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note:
            flash('fill the note field!',category='error')
        else:
            existNote = Note.query.filter_by(data=note).first()
            if existNote:
                flash('Note already exists, type something different!',category='error')
            elif len(note) < 10:
                flash('Note is too short min 10 charaters!',category='error')
            else:
                new_note = Note(data=note,user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added Successfully!',category='success')
                
    return render_template('home.html',user=current_user)


@views.route('/delete-note', methods=['POST','GET'])
def delete_note():
    if request.method == 'POST':
        note_id = request.form.get('delete_note')
        existNote = Note.query.filter_by(id=note_id).first()
        if existNote:
            if existNote.user_id == current_user.id:
                db.session.delete(existNote)
                db.session.commit()
                flash('Note Deleted Successfully',category='success')
        else:
            flash('This note not exists in database!',category='error')
    return redirect(url_for('views.home'))



