from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from flask_login import current_user, login_required, logout_user
from app.models import Dictionary
from app.dictionary.forms import Add_Word
from app import db


dictionary = Blueprint('dictionary', __name__)


@dictionary.route('/dictionary/add_word', methods=['GET', 'POST'])
def add_word():
    form = Add_Word()
    
    if form.validate_on_submit():
        add_words = Dictionary(english_word = form.english_word.data.lower(), 
                            german_article=form.german_article.data.lower(), 
                            german_word=form.german_word.data.lower(), 
                            user_id =current_user.id)
        db.session.add(add_words)
        db.session.commit()
        
        return redirect(url_for('main.home'))
    else:
        flash('Error: enter a valid english and german word', 'warning')

    return render_template('add_word.html',title='New Word', form = form)

@dictionary.route('/dictionary/<int:word_id>', methods= ['GET', 'POST'])
def selected_word(word_id):
    word = Dictionary.query.get_or_404(word_id)
    return render_template('selected_word.html', title= word.english_word, word = word)

@dictionary.route('/dictionary/<int:word_id>/update', methods=['GET', 'POST'])
@login_required
def update_word(word_id):
    word = Dictionary.query.get_or_404(word_id)
    form = Add_Word()

    if word.word != current_user:
        abort(403)
    if form.validate_on_submit():
        word.english_word = form.english_word.data
        word.german_article = form.german_article.data
        word.german_word = form.german_word.data
        db.session.commit()
        return redirect(url_for('dictionary.selected_word', word_id = word.id))
    elif request.method == 'GET':
        form.english_word.data = word.english_word
        form.german_article.data = word.german_article
        form.german_word.data = word.german_word 
    
    return render_template('update.html', title='Update', form = form, word = word)

@dictionary.route('/dictionary/<int:word_id>/delete')
def delete_word(word_id):
    word = Dictionary.query.get_or_404(word_id)
    if word.word != current_user:
        abort(403)
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for('main.home'))
