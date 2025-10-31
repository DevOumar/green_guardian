# pages/3_📜_Historique_des_tris.py
import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO

# --- CONFIG DE LA PAGE ---
st.set_page_config(page_title="📜 Historique des tris – GreenGuardian", page_icon="🗂️", layout="wide")
# Appliquer le style CSS global
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Barre de navigation personnalisée
st.markdown("""
<div class="navbar">
    <h1>🌿 <span>GreenGuardian</span></h1>
    <p>IA pour un monde plus propre ♻️</p>
</div>
""", unsafe_allow_html=True)

st.title("📜 Historique des tris – GreenGuardian")

st.markdown("""
Retrouve ici **toutes les analyses effectuées** 🧠  
Tu peux consulter :
- les images des déchets analysés,
- la prédiction du modèle,
- la confiance,
- et la date du tri ♻️
""")

# --- CHEMINS DE DONNÉES ---
history_file = "history.csv"

# --- VÉRIFICATION ---
if not os.path.exists(history_file):
    st.info("Aucune donnée disponible pour le moment. Fais d'abord quelques prédictions dans 🧠 *Analyse d'image*.")
    st.stop()

df = pd.read_csv(history_file)

if df.empty:
    st.warning("Ton historique est encore vide. Fais une première analyse d’image !")
    st.stop()

# Trier du plus récent au plus ancien
df = df.sort_values(by="timestamp", ascending=False).reset_index(drop=True)

# --- BARRE D'OPTIONS ---
st.sidebar.header("⚙️ Options d'affichage")

# Filtre par catégorie
categories = ["Toutes"] + sorted(df["prediction"].unique().tolist())
selected_cat = st.sidebar.selectbox("🧩 Filtrer par catégorie", categories)

# Filtre par date
dates = sorted(df["timestamp"].str[:10].unique().tolist())
selected_date = st.sidebar.selectbox("📅 Filtrer par date", ["Toutes"] + dates)

# Appliquer les filtres
filtered_df = df.copy()
if selected_cat != "Toutes":
    filtered_df = filtered_df[filtered_df["prediction"] == selected_cat]
if selected_date != "Toutes":
    filtered_df = filtered_df[filtered_df["timestamp"].str.startswith(selected_date)]

# --- BOUTONS D'ACTION ---
col1, col2, col3 = st.columns([2, 1, 1])

# Télécharger l'historique
csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

col2.download_button(
    label="⬇️ Télécharger l’historique",
    data=csv_data,
    file_name="historique_green_guardian.csv",
    mime="text/csv"
)

# Supprimer l’historique
if col3.button("🗑️ Supprimer tout l’historique"):
    st.warning("⚠️ Cette action supprimera définitivement toutes les données.")
    confirm = st.checkbox("Je confirme la suppression", key="confirm_delete")
    if confirm:
        os.remove(history_file)
        st.success("✅ Historique supprimé avec succès ! Recharge la page pour voir le changement.")
        st.stop()

# --- AFFICHAGE DES CARTES ---
if filtered_df.empty:
    st.warning("Aucune correspondance trouvée avec tes filtres.")
else:
    st.markdown(f"### 🧾 Résultats ({len(filtered_df)} éléments)")
    for i, row in filtered_df.iterrows():
        cols = st.columns([1, 2])
        image_path = row["image_path"]

        if os.path.exists(image_path):
            img = Image.open(image_path)
            cols[0].image(img, caption=f"{row['prediction']} ({row['confidence']}%)", width=180)

        cols[1].markdown(f"""
        **Catégorie :** `{row['prediction']}`  
        **Confiance :** {row['confidence']} %  
        **Date :** {row['timestamp']}  
        """)
        cols[1].markdown("---")

st.success("✅ Historique chargé avec succès ! Continue de trier éco-intelligemment 🌿")
