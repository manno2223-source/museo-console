import sqlite3

def crea_il_database():
    # Connessione al file database.db (se non esiste, viene creato da zero)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    print("Creazione della tabella in corso...")
    
    # Creazione della tabella 'console' con i 5 campi richiesti dalla traccia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS console (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            produttore TEXT NOT NULL,
            anno_uscita INTEGER NOT NULL,
            generazione TEXT NOT NULL,
            descrizione TEXT
        )
    ''')

    # Controllo se il database è già popolato, altrimenti inserisce i 10 record minimi richiesti
    cursor.execute("SELECT COUNT(*) FROM console")
    conteggio = cursor.fetchone()[0]
    
    if conteggio == 0:
        print("Inserimento dei 10 record iniziali...")
        console_iniziali = [
            ("Magnavox Odyssey", "Magnavox", 1972, "1a Generazione", "La prima console domestica della storia."),
            ("Atari 2600", "Atari", 1977, "2a Generazione", "Ha reso popolari i giochi su cartuccia."),
            ("NES", "Nintendo", 1983, "3a Generazione", "Ha rivitalizzato l'industria dei videogiochi negli anni '80."),
            ("Sega Mega Drive", "Sega", 1988, "4a Generazione", "La storica rivale del Super Nintendo."),
            ("PlayStation", "Sony", 1994, "5a Generazione", "Ha introdotto la grafica 3D nel mercato di massa."),
            ("Nintendo 64", "Nintendo", 1996, "5a Generazione", "Famosa per capolavori rivoluzionari come Super Mario 64."),
            ("PlayStation 2", "Sony", 2000, "6a Generazione", "La console domestica più venduta di tutti i tempi."),
            ("Xbox 360", "Microsoft", 2005, "7a Generazione", "Ha rivoluzionato l'infrastruttura del gioco online."),
            ("Nintendo Switch", "Nintendo", 2017, "8a Generazione", "Innovativa console ibrida sia fissa che portatile."),
            ("PlayStation 5", "Sony", 2020, "9a Generazione", "Console moderna con grafica in 4K e caricamenti ultra-rapidi.")
        ]
        
        cursor.executemany('''
            INSERT INTO console (nome, produttore, anno_uscita, generazione, descrizione) 
            VALUES (?, ?, ?, ?, ?)
        ''', console_iniziali)
        
        conn.commit()
        print("Database creato e popolato con successo!")
    else:
        print(f"Il database esiste già e contiene già {conteggio} console.")

    # Chiude la connessione
    conn.close()

if __name__ == '__main__':
    crea_il_database()