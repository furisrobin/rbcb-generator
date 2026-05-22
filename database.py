import sqlite3

def init_db():
    conn = sqlite3.connect('branding.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS designs
                 (id INTEGER PRIMARY KEY, company TEXT, industry TEXT, 
                  slogan TEXT, hero_text TEXT, features TEXT)''')
    conn.commit()
    conn.close()

def save_design(company, industry, slogan, hero_text, features):
    conn = sqlite3.connect('branding.db')
    c = conn.cursor()
    # Převedeme seznam vlastností na text, aby se vešel do databáze
    features_str = ", ".join(features)
    c.execute("INSERT INTO designs (company, industry, slogan, hero_text, features) VALUES (?, ?, ?, ?, ?)",
              (company, industry, slogan, hero_text, features_str))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('branding.db')
    c = conn.cursor()
    c.execute("SELECT * FROM designs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows