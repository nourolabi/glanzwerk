# Glanzwerk Rheinland - Digitales Rechnungssystem: Projektdokumentation

## 1. Einführung

Dieses Dokument beschreibt die Entwicklung eines digitalen Rechnungssystems für die Autowaschanlage Glanzwerk Rheinland in Neuwied. Ziel war es, eine benutzerfreundliche Web-Anwendung zu erstellen, die professionelle PDF-Rechnungen im Corporate Design generiert und über Streamlit Cloud öffentlich zugänglich ist.

## 2. Projektziele

- **Digitalisierung des Fakturierungsprozesses:** Ersetzen der manuellen Rechnungserstellung durch eine automatisierte Web-Anwendung.
- **Professionelle PDF-Rechnungen:** Generierung von Rechnungen im Glanzwerk-Design, inklusive Logo, Adresse, Farben, Tabellenstruktur und Schriftarten.
- **Benutzerfreundliche Weboberfläche:** Eine intuitive Streamlit-Anwendung für die einfache Eingabe von Kundendaten und Dienstleistungen.
- **Öffentliche Verfügbarkeit:** Hosting der Anwendung auf Streamlit Cloud, um sie ohne Installation auf dem Endgerät zugänglich zu machen.
- **Open-Source:** Bereitstellung des Codes auf GitHub.

## 3. Implementierte Funktionen

Die Anwendung umfasst die folgenden Kernfunktionen:

- **Kundendaten-Eingabe:** Felder für Kundenname und KFZ-Kennzeichen.
- **Dienstleistungsauswahl:** Eine vordefinierte Liste von 15 Dienstleistungen, die ausgewählt werden können.
- **Manuelle Dienstleistungen:** Möglichkeit, zusätzliche Dienstleistungen mit individuellen Preisen und Mengen hinzuzufügen.
- **Anpassbare Preise und Mengen:** Für jede ausgewählte oder manuell hinzugefügte Dienstleistung können Preis und Menge angepasst werden.
- **Optionaler Rabatt:** Ein Feld zur Eingabe eines prozentualen Rabatts.
- **Zahlungsarten:** Auswahlmöglichkeiten für Bar, Überweisung und PayPal.
- **Automatische Berechnung:** Zwischensumme, Mehrwertsteuer (19%) und Gesamtsumme werden automatisch berechnet.
- **PDF-Generierung:** Erstellung einer PDF-Rechnung auf Knopfdruck, die alle eingegebenen Daten und Berechnungen enthält.
- **Corporate Design:** Das generierte PDF entspricht dem visuellen Stil der Glanzwerk Word-Vorlage, inklusive Logo, Adresse und spezifischen Schriftarten (DejaVuSans für Unicode-Unterstützung).
- **Datenbank:** Eine SQLite-Datenbank (`glanzwerk.db`) speichert die generierten Rechnungen für eine einfache Nachverfolgung. (Hinweis: In Streamlit Cloud ist diese Datenbank flüchtig, für persistente Speicherung wäre eine externe Datenbank erforderlich).

## 4. Technische Umsetzung

### 4.1. Technologien

- **Frontend:** Streamlit (Python-Framework für Web-Anwendungen)
- **PDF-Generierung:** `fpdf2` (Python-Bibliothek)
- **Datenbank:** SQLite3 (Python-Standardbibliothek)
- **Versionierung:** Git / GitHub

### 4.2. Projektstruktur

```
glanzwerk-invoice-system/
├── app.py                     # Haupt-Streamlit-Anwendung
├── pdf_generator_new.py       # Modul für die PDF-Generierung
├── requirements.txt           # Python-Abhängigkeiten
├── Glanzwerk_logo_no_background.png # Glanzwerk Logo
├── fonts/                     # Verzeichnis für Schriftarten
│   ├── DejaVuSans.ttf
│   └── DejaVuSans-Bold.ttf
├── glanzwerk.db               # SQLite-Datenbank (wird bei erster Ausführung erstellt)
├── README.md                  # Projektbeschreibung und Installationsanleitung
└── streamlit_deployment_guide.md # Anleitung für Streamlit Cloud Deployment
```

### 4.3. Code-Details

- **`app.py`:**
    - Initialisiert die SQLite-Datenbank und erstellt die `invoices`-Tabelle, falls sie nicht existiert.
    - Definiert die Streamlit-Oberfläche mit Eingabefeldern und Schaltflächen.
    - Verarbeitet Benutzereingaben und Berechnungen.
    - Ruft `pdf_generator_new.py` auf, um die PDF-Rechnung zu erstellen.
    - Speichert die Rechnungsdaten in der Datenbank.
    - Bietet einen Download-Link für die generierte PDF.

- **`pdf_generator_new.py`:**
    - Erbt von `FPDF` und überschreibt die `header`-Methode, um das Glanzwerk-Logo und die Adresse einzufügen.
    - Verwendet `DejaVuSans` Schriftarten, um die korrekte Darstellung von deutschen Umlauten in der PDF zu gewährleisten.
    - Zeichnet die Rechnungstabelle, Dienstleistungsdetails, Zwischensummen, Mehrwertsteuer und Gesamtsumme.
    - Fügt Fußzeileninformationen hinzu.

- **`requirements.txt`:**
    - Enthält die notwendigen Python-Pakete für die Ausführung der Anwendung, insbesondere `streamlit` und `fpdf2`.

## 5. Lokale Installation und Ausführung

Eine detaillierte Anleitung zur lokalen Installation und Ausführung finden Sie in der `README.md` Datei im Projektverzeichnis.

## 6. Deployment auf Streamlit Cloud

Eine detaillierte Anleitung zum Deployment auf Streamlit Cloud finden Sie in der `streamlit_deployment_guide.md` Datei im Projektverzeichnis.

## 7. Zukünftige Erweiterungen

- **Benutzerauthentifizierung:** Implementierung eines Login-Systems für den Zugriff auf die Anwendung.
- **Kundenverwaltung:** Eine Datenbank für wiederkehrende Kunden, um deren Daten automatisch zu laden.
- **Dienstleistungsverwaltung:** Eine Oberfläche zur einfachen Verwaltung der vordefinierten Dienstleistungen und ihrer Preise.
- **Rechnungsarchiv:** Eine erweiterte Ansicht der gespeicherten Rechnungen mit Such- und Filterfunktionen.
- **E-Mail-Versand:** Option zum direkten Versenden der Rechnung per E-Mail an den Kunden.
- **Integration mit externen Datenbanken:** Für persistente Datenspeicherung in einer Cloud-Umgebung.

## 8. Fazit

Das Glanzwerk Rheinland Digitale Rechnungssystem bietet eine robuste und benutzerfreundliche Lösung für die effiziente Erstellung professioneller Rechnungen. Durch die Nutzung von Streamlit und `fpdf2` konnte eine leistungsstarke Anwendung mit einem ansprechenden Corporate Design realisiert werden, die einfach zu bedienen und bereitzustellen ist.

