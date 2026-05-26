from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'database.db'

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Legge le console salvate nel database
    cursor.execute("SELECT * FROM console ORDER BY anno_uscita ASC")
    tutte_le_console = cursor.fetchall()
    conn.close()
    return render_template('index.html', consoles=tutte_le_console)

@app.route('/aggiungi', methods=['GET', 'POST'])
def aggiungi():
    if request.method == 'POST':
        nome = request.form['nome']
        produttore = request.form['produttore']
        anno_uscita = request.form['anno_uscita']
        generazione = request.form['generazione']
        descrizione = request.form['descrizione']
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO console (nome, produttore, anno_uscita, generazione, descrizione) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, produttore, anno_uscita, generazione, descrizione))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    # Avvio pulito senza ricaricamenti strani che bloccano Windows
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)