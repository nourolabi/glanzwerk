import streamlit as st
import sqlite3
import tempfile
import os
from datetime import datetime
from fpdf import FPDF
import base64
from pdf_generator_new import generate_invoice_pdf_new

# Konfiguration der Streamlit-Seite
st.set_page_config(
    page_title="Glanzwerk Rechnungssystem",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS für das Design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2d5016 0%, #5a9216 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .invoice-preview {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #5a9216;
        margin-top: 2rem;
    }
    
    .discount-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #5a9216 0%, #2d5016 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(90, 146, 22, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Logo anzeigen
logo_path = "Glanzwerk_logo_no_background.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()
else:
    logo_base64 = ""
# Service-Preise
SERVICE_PRICES = {
    'Außenreinigung per Hand': 25.0,
    'Felgenreinigung & Flugrostentfernung': 15.0,
    'Innenraumreinigung': 30.0,
    'Lederreinigung & -pflege': 40.0,
    'Lederreparatur': 60.0,
    'Polster- & Teppichreinigung': 35.0,
    'Scheibenreinigung innen & außen': 10.0,
    'Lackpolitur & Glanzversiegelung': 80.0,
    'Nano-Keramik-Versiegelung': 150.0,
    'Motorraumreinigung': 25.0,
    'Geruchsneutralisierung & Ozonbehandlung': 45.0,
    'Tierhaarentfernung': 20.0,
    'Hagelschaden- und Dellenentfernung (Ausbeulen ohne Lackieren)': 100.0,
    'Auto Folieren': 200.0,
    'Abhol- und Bringservice': 15.0
}

def init_db():
    """Initialisiert die SQLite-Datenbank"""
    conn = sqlite3.connect('glanzwerk.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
                        visit_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    conn.commit()
    conn.close()

def add_customer(name):
    """Fügt einen Kunden hinzu oder gibt die ID zurück, falls er bereits existiert"""
    conn = sqlite3.connect('glanzwerk.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO customers (name) VALUES (?)', (name,))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        # Kunde existiert bereits, gib seine ID zurück
        c.execute('SELECT id FROM customers WHERE name = ?', (name,))
        return c.fetchone()[0]
    finally:
        conn.close()

def record_visit(customer_id):
    """Zeichnet einen Besuch auf"""
    conn = sqlite3.connect('glanzwerk.db')
    c = conn.cursor()
    c.execute('INSERT INTO visits (customer_id, visit_date) VALUES (?, DATE(\'now\'))', (customer_id,))
    conn.commit()
    conn.close()

def get_customer_visits(customer_id):
    """Gibt die Anzahl der Besuche eines Kunden zurück"""
    conn = sqlite3.connect('glanzwerk.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM visits WHERE customer_id = ?', (customer_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def create_download_link(file_path, filename):
    """Erstellt einen Download-Link für eine Datei"""
    with open(file_path, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; font-weight: 600; display: inline-block; margin-top: 1rem;">📥 PDF-Rechnung herunterladen</a>'
    return href

def main():
    # Initialisiere Datenbank
    init_db()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1><img src="data:image/png;base64,{logo_base64}" style="height: 50px; vertical-align: middle; margin-right: 10px;"> Glanzwerk Rechnungssystem</h1>
        <p>Professionelle Fahrzeugpflege - Schnelle Rechnungserstellung</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Eingabeformular
    with st.form("invoice_form"):
        st.subheader("📋 Rechnungsdaten eingeben")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("👤 Kundenname", placeholder="Geben Sie den Kundennamen ein")
        
        with col2:
            vehicle_number = st.text_input("🚙 Fahrzeugnummer / Kennzeichen", placeholder="z.B. NR-AB 1234")
        
        service = st.selectbox(
            "🧽 Gewählte Leistung",
            options=list(SERVICE_PRICES.keys()),
            format_func=lambda x: f"{x} ({SERVICE_PRICES[x]:.2f}€)"
        )
        
        submitted = st.form_submit_button("📄 Rechnung generieren")
    
    if submitted and customer_name and vehicle_number and service:
        # Kunde hinzufügen oder abrufen
        customer_id = add_customer(customer_name)
        
        # Besuch aufzeichnen
        record_visit(customer_id)
        
        # Gesamtbesuche für Rabattberechnung abrufen
        total_visits = get_customer_visits(customer_id)
        
        # Preisberechnung
        net_price = SERVICE_PRICES[service]
        tax_rate = 0.19
        tax_amount = net_price * tax_rate
        gross_price = net_price + tax_amount
        
        # 10% Rabatt nach 5 Besuchen anwenden
        discount_applied = total_visits >= 5
        discount_amount = 0
        if discount_applied:
            discount_amount = gross_price * 0.10
        
        total_price = gross_price - discount_amount
        
        # Rechnungsdaten für PDF-Generierung speichern
        invoice_data = {
            'customer_name': customer_name,
            'vehicle_number': vehicle_number,
            'service': service,
            'net_price': net_price,
            'tax_amount': tax_amount,
            'discount_applied': discount_applied,
            'discount_amount': discount_amount,
            'total_price': total_price,
            'total_visits': total_visits
        }
        
        # Rechnungsvorschau anzeigen
        st.markdown("""
        <div class="invoice-preview">
            <h2>📋 Rechnungsvorschau</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Kunde:** {customer_name}")
            st.write(f"**Fahrzeug:** {vehicle_number}")
            st.write(f"**Leistung:** {service}")
        
        with col2:
            st.write(f"**Nettobetrag:** {net_price:.2f}€")
            st.write(f"**MwSt (19%):** {tax_amount:.2f}€")
            if discount_applied:
                st.markdown(f"**Stammkundenrabatt:** -{discount_amount:.2f}€ <span class='discount-badge'>🎉 10% Rabatt!</span>", unsafe_allow_html=True)
        
        st.markdown(f"### **Gesamtbetrag: {total_price:.2f}€**")
        
        if discount_applied:
            st.success(f"🎊 Herzlichen Glückwunsch! Sie sind Stammkunde mit {total_visits} Besuchen und erhalten 10% Rabatt!")
        
        # PDF generieren mit neuem Design
        pdf_path = generate_invoice_pdf_new(invoice_data)
        filename = f"Rechnung_{customer_name.replace(' ', '_')}.pdf"
        
        # Download-Link erstellen
        download_link = create_download_link(pdf_path, filename)
        st.markdown(download_link, unsafe_allow_html=True)
        
        # Temporäre Datei nach dem Download löschen
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
    
    elif submitted:
        st.error("Bitte füllen Sie alle Felder aus!")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>💻 Entwickelt von <strong>Mazen Design</strong> | Glanzwerk Rheinland - Krasnaer Str. 1, 56566 Neuwied</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

