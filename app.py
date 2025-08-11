from flask import Flask, render_template, request, redirect
import sqlite3, random

app = Flask(__name__)

# Create the database if it doesn't exist
def init_db():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM quotes")
    quotes = [row[0] for row in cursor.fetchall()]
    conn.close()

    if quotes:
        random_quote = random.choice(quotes)
    else:
        random_quote = "No quotes yet. Add one!"

    return render_template("index.html", quote=random_quote)

@app.route("/add", methods=["GET", "POST"])
def add_quote():
    if request.method == "POST":
        quote = request.form["quote"]
        if quote.strip():
            conn = sqlite3.connect("quotes.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quotes (text) VALUES (?)", (quote,))
            conn.commit()
            conn.close()
        return redirect("/")
    return render_template("add_quote.html")

if __name__ == "__main__":
    app.run(debug=True)