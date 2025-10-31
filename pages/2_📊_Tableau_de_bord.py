# pages/2_📊_Tableau_de_bord.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------
st.set_page_config(page_title="📊 Tableau de bord – GreenGuardian", page_icon="🌿", layout="wide")
st.title("📊 Tableau de bord – GreenGuardian")

st.markdown("""
Bienvenue sur ton **tableau de bord écologique** 🌿  
Ici, tu peux suivre :
- ton **impact environnemental global**,  
- la **répartition des déchets triés**,  
- et ton **évolution dans le temps** 💪
""")

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
if not os.path.exists("history.csv"):
    st.info("Aucune donnée disponible pour le moment. Analyse d’abord quelques déchets pour générer des statistiques 📸")
    st.stop()

df = pd.read_csv("history.csv")

if df.empty:
    st.warning("Ton historique est encore vide. Analyse quelques déchets pour voir ton tableau de bord s’animer 💚")
    st.stop()

# -----------------------------
# MÉTRIQUES GLOBALES
# -----------------------------
total_predictions = len(df)
avg_confidence = df["confidence"].mean()
most_common = df["prediction"].mode()[0]

# Impact écologique estimé
eco_points = round(total_predictions * 2.5, 1)
co2_saved = round(total_predictions * 0.08, 2)
trees_saved = round(co2_saved / 20, 3)

col1, col2, col3 = st.columns(3)
col1.metric("♻️ Total de tris", total_predictions)
col2.metric("🌿 Points écologiques", eco_points)
col3.metric("🌳 CO₂ économisé (kg)", co2_saved)

st.progress(min(eco_points / 100, 1.0))
st.caption(f"≈ {trees_saved} arbre(s) sauvé(s) 🌱")

# -----------------------------
# NIVEAU ÉCOLOGIQUE
# -----------------------------
if total_predictions < 20:
    level = "🪴 Éco-débutant"
    desc = "Tu commences ton aventure verte ! Continue à apprendre à bien trier 🌿"
elif total_predictions < 50:
    level = "🌿 Éco-citoyen"
    desc = "Super ! Tes gestes font déjà une vraie différence 💪"
elif total_predictions < 100:
    level = "🌳 Protecteur de la planète"
    desc = "Tu es un modèle pour ta communauté 🌎"
else:
    level = "🌎 Gardien suprême de la Terre"
    desc = "Incroyable ! Ton engagement écologique est exemplaire 🔥"

st.markdown("---")
st.markdown(f"### 🏆 Ton niveau actuel : **{level}**")
st.info(desc)

# -----------------------------
# STATISTIQUES DÉTAILLÉES
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Catégorie la plus triée", most_common.capitalize())
col2.metric("Confiance moyenne", f"{avg_confidence:.1f}%")
col3.metric("Jour le plus actif", df['timestamp'].str[:10].mode()[0])
col4.metric("Dernier tri", df['timestamp'].iloc[-1][:10])

st.markdown("---")

# -----------------------------
# RÉPARTITION DES CATÉGORIES
# -----------------------------
st.subheader("📦 Répartition des déchets triés")

category_counts = df["prediction"].value_counts()
fig, ax = plt.subplots(figsize=(6, 4))
ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# -----------------------------
# ÉVOLUTION DANS LE TEMPS
# -----------------------------
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    trend = df.groupby("date").size()

    st.subheader("📈 Évolution du tri dans le temps")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(trend.index, trend.values, marker="o", linewidth=2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Nombre de tris")
    ax2.set_title("Progression quotidienne du tri ♻️")
    st.pyplot(fig2)

# -----------------------------
# MESSAGE FINAL
# -----------------------------
st.success("👏 Continue de trier intelligemment ! Chaque geste compte 💚")
