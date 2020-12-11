#  Flask wird genutzt, um die Webanwendung in Python zu erstellen.
#  render_template ist eine Flask-Funktion, die eine HTML-Seite rendert, die im "templates" Ordner sein muss.
from flask import Flask, render_template
#  Importiere send_mail() aus der Datei main.py
from main import send_mail
#  Importiere die config.py (siehe main.py Kommentar)
import config
app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/trigger_event", methods=["GET", "POST"])
def form():
    send_mail(config.empfaenger)
    return "Die E-Mail wurde erfolgreich versendet."

if __name__ == "__main__":
  app.run(debug=True)