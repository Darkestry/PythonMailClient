# Das Modul "smtplib" definiert eine Simple Mail Transfer Protocol-Client Session,
# die dazu genutzt werden kann von internetfähigen Geräten E-Mails zu versenden
import smtplib

# Mit dem Modul "email.mime" kann man mehrteilige Emails mit Änhangen (z.B. Text- und Bilddateien) erstellen.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

# Flask ist ein Web-Framework mit vielen Tools und Funktionen.
# Wir erstellen eine Datei "config.py" in unserem Root-Verzeichnis und definieren jeweils eine Variable pro Zeile.
# Nun importieren wir diese in unsere Applikation und können mit den in "config.py" gespeicherten Daten interagieren.
import config

# "PRAW" steht für "Python Reddit API Wrapper". Dieses Modul ermöglicht den Zugriff auf die Reddit API,
# um direkt mit dem Backend kommunizieren zu können.
import praw

# Mit dem Modul "Schedule" können wir Funktionen in festgelegten Intervallen regelmäßig ausführen.
import schedule

# Mit dem Modul "time" können wir zeitbezogene Aufgaben erledigen.
import time

# Reddit Login
# PRAW unterstützt drei Applikationstypen, die auf Reddit registriert werden müssen:
# Web-Applikationen, installierte Applikationen und in unserem Fall: Skript-Applikationen.
# Verwendet wird OAuth 2.0, ein offenes Protokoll, dass eine sichere API-Autorisierung erlaubt.
# Beim Authentifizierungsablauf verwenden wir den "Password Flow"
# Um eine "Password Flow"-Applikation mit PRAW zu verwenden, benötigen wir 5 Informationen:
reddit = praw.Reddit(client_id=config.client_id,  # Die client ID ist ein 14-stelliger String
                     client_secret=config.client_secret,  # Die client secret ist ein 27-stelliger String
                     password=config.password,  # Das Passwort des zur Registrierung verwendeten Reddit Accounts

                     # Ein User-Agent ist ein String, den das Programm angibt, das an ein Webserver eine Anforderung
                     # für ein Asset wie ein Dokument, ein Bild oder eine Webseite stellt.
                     user_agent=config.user_agent,

                     username=config.username)  # Den Benutzernamen des zur Registrierung verwendeten Reddit Accounts

# Wir überprüfen, ob die Authentifikation des Benutzers erfolgreich war.
print("Der Benutzer " + str(reddit.user.me()) + " wurde erfolgreich authentifiziert\n" + 200 * "-")

# Erstellt ein mit "Amd" parametrisiertes Subreddit-Objekt und speichert es.
subreddit = reddit.subreddit("Amd")

# Wir definieren die Variable "hot_amd" und weisen ihr die fünf heißesten Threads des Subreddit-Objekts zu.
hot_amd = subreddit.hot(limit=5)

# Die Variable "submission" wird mit dem Keyword "None" als "null value" definiert, damit wir auf diese auch in der
# show_hottest()-Funktion zugreifen können.
submission = None


# Wir definieren eine Funktion "show_hottest()"
# Speichere Namen und Upvotes der fünf "hottest" Threads und zeige dabei keine Threads, die angepinnt wurden

def show_hottest():
    with open("reddit_hot.txt", "w", encoding="utf-8") as f:  # Erstelle die Textdatei "reddit_hot.txt"
        f.seek(0)  # Lösche alle Daten (da wir mehrmals (alle 30 Minuten) die Funktion aufrufen)

        # definiere die globale Variable "submission", um Daten auch nach Ausführung der Funktion zu erhalten.
        global submission

        # Wir itarieren über die neuesten submissions in hot_amd
        for submission in hot_amd:

            # Mit dem Attribut "stickied" des Objekts "submission" prüfen wir, ob die submission angepinnt wurde.
            if not submission.stickied:

                # Wir formattieren den Text, der in "reddit_hot.txt" geschrieben wird.
                f.write("Titel: {} | Upvotes: {}\n".format(submission.title,
                                                           submission.ups))

        # Zugriff auf Kommentare der hottest Threads
        # Das Attribut "comments" stellt eine Instanz von "CommentForest" bereit
        # Die replace_more() Methode lässt uns Instanzen von "MoreComments" ersetzen
        # Das Argument "limit=0" löscht alle Instanzen von "MoreComments", um die Übersichtlichkeit zu wahren
        submission.comments.replace_more(limit=0)

        # Wir weisen dem Submission-Objekt die Variable "comments" zu und übergeben eine Liste der Kommentare.
        comments = submission.comments.list()

        # Itariere über alle Kommentare, speichere und formattiere Kommentare in "reddit_hot".txt"
        for comment in comments:
            f.write("\n")
            f.write(200 * "-")
            f.write("\n")
            f.write("Parent ID: {}\n".format(comment.parent()))
            f.write("Comment ID: {}\n\n".format(comment.id))
            f.write(comment.body)


# Streame und speichere Namen und Upvotes der neuesten Threads
def show_newest():
    with open("reddit_updates.txt", "w", encoding="utf-8") as f:
        f.seek(0)  # Lösche alle Daten (da wir mehrmals (alle 30 Minuten) die Funktion aufrufen)
        i = 0  # Zählvariable i wird initialisiert

        # Streame submissions im subreddit von "Amd"
        # Greife auf bereits existierende submissions zu und streame eine zeitlang.
        for post in subreddit.stream.submissions():
            # try und except zur Behandlung von Fehlern
            try:
                f.write("Titel: {} | Upvotes: {}\n".format(post.title,  # Schreibe Titel und Upvotes in "reddit_updates"
                                                           post.ups))
                f.write("{} {}".format(300 * "-", "\n"))
                i += 1
                if i == 100:  # Wenn die 100 erreicht sind, höre auf zu streamen bzw. verlasse die Funktion.
                    break
            except Exception as e:  # Erstelle ein Exception-Objekt, damit wir darauf zugreifen können.
                f.write(str(e))   # Logge die Exception in "reddit_updates.txt"
                i += 1
                if i == 100:  # Wenn die 100 erreicht sind, höre auf zu streamen bzw. verlasse die Funktion.
                    break


# Funktion zum Versenden von E-Mails
def send_mail(recipients):
    print("Beginne Nachricht zu erstellen...")
    show_hottest()  # Führe die Funktion aus
    print("Speichere reddit_hot...\nStreame die neuesten Threads...")
    show_newest()  # Führe die Funktion aus
    print("Speichere reddit_updates...")
    time.sleep(5)  # Warte 5 Sekunden

    print("Dateien wurden erfolgreich gespeichert...")

    body = "Dies ist eine mit Python gesendete Nachricht, im Anhang dieser E-Mail finden Sie die neuesten Posts im " \
           "Subreddit von Advanced Micro Devices (AMD) "
    msg = MIMEMultipart()  # Erstelle ein MIMEMultipart-Objekt (eine Art multifunktionale Blaupause für unsere E-Mail)

    msg["Subject"] = "Es gibt Neues zu entdecken auf Reddit!"  # Betreff der E-Mail
    msg["From"] = config.user  # Absender der E-Mail
    msg["To"] = ", ".join(recipients.split(","))  # Empfänger der E-Mail

    msg.attach(MIMEText(body, "plain"))  # Hänge den Body an die E-Mail an.
    fp = open("grapefruit.jpg", "rb")  # Öffne die Bilddatei
    msg_image = MIMEImage(fp.read())  # Lese die Bilddatei ein
    fp.close()  # Schließe die Bilddatei
    msg.attach(msg_image)  # Hänge "grapefruit.jpg" an die E-Mail an.

    print("Bild wurde erfolgreich angehängt...")

    msg_hot = "reddit_hot.txt"
    msg_new = "reddit_updates.txt"
    attachment1 = open(msg_hot, "rb")
    attachment2 = open(msg_new, "rb")

    hot = MIMEBase("application", "octet-stream")
    hot.set_payload(attachment1.read())
    hot.add_header("Content-Disposition", "attachment", filename=msg_hot)

    new = MIMEBase("application", "octet-stream")
    new.set_payload(attachment2.read())
    new.add_header("Content-Disposition", "attachment", filename=msg_new)

    msg.attach(hot)  # Hänge "reddit_hot.txt" an die E-Mail an.
    msg.attach(new)  # Hänge "reddit_updates.txt" an die E-Mail an.

    print("Dateien wurden erfolgreich angehängt...\n")

    server = smtplib.SMTP("smtp.web.de", 587)  # Greife auf den SMTP-Server von web.de über den TLS Port 587 zu.
    server.ehlo()  # EHLO startet die SMTP-Sitzung und identifiziert den Client am Server.
    server.starttls()  # Verschlüsselung mit TLS wird eingeleitet
    server.ehlo()  # EHLO startet die SMTP-Sitzung und identifiziert den Client am Server.
    server.login(config.user, config.password)
    server.send_message(msg)  # Sende E-mail
    print("E-Mail wurde erfolgreich gesendet")
    server.quit()


# Rufe Funktion zur Versendung von E-Mails auf
# Übergebe der Funktion das Argument config.empfaenger
send_mail(config.empfaenger)

# Führe die Funktion zur Versendung einer E-Mail alle 30 Minuten aus.
schedule.every(30).minutes.do(send_mail, config.empfaenger)

while 1:
    schedule.run_pending()  # Führe alle Aufgaben aus, deren Ausführung geplant ist.
    time.sleep(1)
