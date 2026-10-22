import streamlit as st

# Seitentitel
st.title("🎫 IT-Support-Ticket-System (ITSM)")
st.write("Willkommen im internen Service-Desk. Erfasse hier deine IT-Störungen.")

# --- Session State (Daten speichern während der Sitzung) ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

if "staff_load" not in st.session_state:
    st.session_state.staff_load = {"Anna": 0, "Ben": 0}

# --- Funktion zur Priorisierung ---
def calculate_priority(title, description):
    text = (title + " " + description).lower()
    if "ausfall" in text or "kritisch" in text or "server" in text:
        return "Hoch"
    elif "drucker" in text or "passwort" in text:
        return "Niedrig"
    else:
        return "Mittel"

# --- Eingabemaske (Formular) ---
with st.form("ticket_form"):
    st.subheader("Neues Ticket erstellen")
    title = st.text_input("Titel des Problems")
    description = st.text_area("Beschreibung")
    
    submit_button = st.form_submit_button(label="Ticket abschicken")
    
    if submit_button:
        if title and description:
            priority = calculate_priority(title, description)
            assigned_staff = min(st.session_state.staff_load, key=st.session_state.staff_load.get)
            st.session_state.staff_load[assigned_staff] += 1
            
            ticket_id = len(st.session_state.tickets) + 1
            new_ticket = {
                "ID": ticket_id,
                "Titel": title,
                "Beschreibung": description,
                "Priorität": priority,
                "Status": "Offen",
                "Mitarbeiter": assigned_staff
            }
            st.session_state.tickets.append(new_ticket)
            st.success(f"Ticket #{ticket_id} erfolgreich erstellt und an {assigned_staff} zugewiesen!")
        else:
            st.warning("Bitte fülle alle Felder aus.")

# --- Dashboard: Übersicht ---
st.divider()
st.subheader("📊 Aktuelle Ticket-Übersicht im Team")

if st.session_state.tickets:
    st.table(st.session_state.tickets)
else:
    st.info("Bisher wurden noch keine Tickets erstellt.")