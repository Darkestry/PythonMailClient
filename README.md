# PythonMailClient
## Programmierung: Klausuraufgabe
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- Reddit ist ein Social-News-Aggregator, eine Website, auf der registrierte Benutzer Inhalte einstellen bzw. anbieten können. 
- Ein Inhalt kann entweder aus einem Link, einem Video, einem Bild, einer Umfrage oder einem Textbeitrag bestehen. 
- Andere Benutzer können die Beiträge als positiv oder negativ beurteilen.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- Das Skript kommuniziert mittels OAuth 2.0 über die Reddit API mit dem Backend von Reddit. 
- Auf das Subreddit von AMD wird im Skript zugegriffen (Z. 46). 
- Um ein anderes Subreddit auszuwählen, muss nur der String bearbeitet werden. 
- Dabei schreibt und speichert die Applikation Titel und Upvotes der hottest Subreddit-Threads, die nicht angepinnt sind und deren Kommentare in einer formatierten Textdatei "reddit_hot.txt".
- Weiter werden die neuesten Subreddit-Threads mit Titel und Upvotes in Echtzeit gestreamt und in eine formatierte Textdatei "reddit_updates.txt" geschrieben und gespeichert.
- Daraufhin wird eine E-Mail mit Bild- und Textdatei-Anhängen erstellt und an die in config.py definierte(n) E-Mail Adresse(n) versendet.

- Es wird mit Flask gearbeitet, das onClick event ist hierbei ein <form> Element mit einem Button auf einer Website, der gedrückt werden muss.
- Um auf die Website zu gelangen, bitte das Terminal öffnen und "python server.py" ausführen.
- Danach ist die Website hier: http://127.0.0.1:5000/ erreichbar.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- In config.py sind alle sensiblen Daten gespeichert.
