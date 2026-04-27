import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Innovation & Sourcing",
    page_icon="🚀",
    layout="wide"
)

# 1. CONNEXION À GOOGLE SHEETS
# Note : L'URL de ton Sheet devra être renseignée dans le fichier secrets de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600) # Rafraîchit les données toutes les 10 minutes
def get_data():
    return conn.read()

try:
    df = get_data()
except Exception as e:
    st.error("Erreur de connexion au Google Sheets. Vérifiez l'URL et les accès.")
    st.stop()

# 2. BARRE LATÉRALE (FILTRES)
st.sidebar.title("🔍 Filtres de Recherche")

# Filtre Régions
regions = ["Île-de-France", "Hauts-de-France"]
selected_regions = st.sidebar.multiselect("Régions", regions, default=regions)

# Filtre Postes
postes = ["Directeur Innovation", "Chargé de Sourcing", "Open Innovation Project Manager"]
selected_postes = st.sidebar.multiselect("Postes cibles", postes, default=postes)

# Filtre Contrat
contrats = st.sidebar.multiselect("Type de contrat", ["CDI", "CDD", "Alternance"], default=["CDI"])

# Filtre Salaire
min_salary = st.sidebar.slider("Salaire minimum (€/an)", 30000, 150000, 45000, step=5000)

# 3. LOGIQUE DE FILTRAGE
mask = (
    df['Region'].isin(selected_regions) & 
    df['Poste'].isin(selected_postes) & 
    df['Contrat'].isin(selected_contrat) &
    (df['Salaire'] >= min_salary)
)
filtered_df = df[mask]

# 4. AFFICHAGE DU DASHBOARD
st.title("🎯 Opportunités Innovation & Sourcing")
st.subheader(f"📍 Zones : {', '.join(selected_regions)}")

# Métriques rapides
col_m1, col_m2 = st.columns(2)
col_m1.metric("Offres trouvées", len(filtered_df))
col_m2.metric("Salaire Moyen (€)", int(filtered_df['Salaire'].mean()) if not filtered_df.empty else 0)

st.divider()

if filtered_df.empty:
    st.warning("Aucune offre ne correspond à vos filtres actuels.")
else:
    # Affichage sous forme de cartes interactives
    for index, row in filtered_df.iterrows():
        with st.expander(f"✨ {row['Poste']} - {row['Entreprise']} ({row['Lieu']})"):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.write(f"**📍 Localisation :** {row['Lieu']} ({row['Region']})")
                st.write(f"**📅 Date :** {row['Date']}")
            with c2:
                st.write(f"**📝 Contrat :** {row['Contrat']}")
                st.write(f"**💰 Salaire :** {row['Salaire']} €")
            with c3:
                st.link_button("Postuler sur l'offre", row['Lien'], use_container_width=True)
