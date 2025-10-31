# app.py — page d'accueil principale
import streamlit as st

st.set_page_config(
    page_title="GreenGuardian ♻️",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menu latéral
st.sidebar.title("🌿 GreenGuardian")
st.sidebar.markdown("### Menu de navigation")
st.sidebar.info("Bienvenue sur la plateforme de tri écologique intelligente ♻️")

# Page d'accueil principale
st.title("🌿 Bienvenue sur GreenGuardian")
st.markdown("""
Bienvenue sur **GreenGuardian**, ton assistant intelligent pour un tri responsable des déchets ♻️  
Utilise le menu à gauche pour naviguer entre les différentes fonctionnalités :

- 🧠 **Analyse d'image** → Téléverse une photo pour identifier automatiquement le type de déchet.
- 📊 **Tableau de bord** → Visualise tes statistiques de tri et ton impact écologique.
- 📜 **Historique** → Consulte la liste de tes précédentes prédictions.
- 🌍 **Carte de tri** → Découvre les points de recyclage proches de toi.
- 🎓 **Quiz écologique** → Teste tes connaissances sur le tri et l’écologie.
""")

st.success("🌱 Commence dès maintenant en sélectionnant une page dans le menu à gauche.")
