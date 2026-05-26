from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# CONFIGURAZIONE DEI PERCORSI PER EVITARE IL CRASH SU VERCEL
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
handler = app

DB_PATH = os.path.join(base_dir, 'database.db')

CONSOLE_MEMORIA = [
    (1, "PlayStation 1", "Sony", 1994, "5a Generazione", "La console che ha portato il 3D nelle case di tutti."),
    (2, "Nintendo 64", "Nintendo", 1996, "5a Generazione", "Rivoluzione totale con Super Mario 64 e i 64 bit."),
    (3, "PlayStation 2", "Sony", 2000, "6a Generazione", "La console più venduta della storia dei videogiochi.")
]

@app.route('/')
def index():
    if os.environ.get('VERCEL'):
        return render_template('index.html', consoles=CONSOLE_MEMORIA)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM console ORDER BY anno_uscita ASC")
        tutte_le_console = cursor.fetchall()
        conn.close()
        return render_template('index.html', consoles=tutte_le_console)
    except Exception:
        return render_template('index.html', consoles=CONSOLE_MEMORIA)

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    nome = request.form['nome']
    produttore = request.form['produttore']
    anno_uscita = request.form['anno_uscita']
    generazione = request.form['generazione']
    descrizione = request.form['descrizione']
    
    if os.environ.get('VERCEL'):
        nuovo_id = len(CONSOLE_MEMORIA) + 1
        CONSOLE_MEMORIA.append((nuovo_id, nome, produttore, int(anno_uscita), generazione, descrizione))
        return redirect(url_for('index'))
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO console (nome, produttore, anno_uscita, generazione, descrizione) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, produttore, anno_uscita, generazione, descrizione))
        conn.commit()
        conn.close()
    except Exception:
        nuovo_id = len(CONSOLE_MEMORIA) + 1
        CONSOLE_MEMORIA.append((nuovo_id, nome, produttore, int(anno_uscita), generazione, descrizione))
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)