#  Flask wird genutzt, um die Webanwendung in Python zu erstellen.
#  render_template ist eine Flask-Funktion, die eine HTML-Seite rendert, die im "templates" Ordner sein muss.
#  Importiere Flask und render_template
from flask import Flask, render_template
#  Importiere send_mail() aus der Datei main.py
from main import send_mail
#  Importiere die config.py (siehe main.py Kommentar)
import config

#  Erstelle eine Instanz der Flask-Klasse
app = Flask(__name__)

#  Verwende  den route()-Dekorator, um Flask mitzuteilen, welche URL unsere Funktion auslösen soll.
#  Rendere die index.html
@app.route("/")
def index():
  return render_template("index.html")


#  Verwende  den route()-Dekorator, um Flask mitzuteilen, welche URL unsere Funktion auslösen soll.
#  Wenn das Formular submitted wird, führe send_mail() aus.
#  Eine GET-Nachricht wird gesendet und der Server gibt Daten zurück.
#  Die POST-Methode wird verwendet, um HTML-Formulardaten an den Server zu senden.
@app.route("/trigger_event", methods=["GET", "POST"])
def form():
    send_mail(config.empfaenger)
    return "Die E-Mail wurde erfolgreich versendet."

#  Debugging
if __name__ == "__main__":
  app.run(debug=True)