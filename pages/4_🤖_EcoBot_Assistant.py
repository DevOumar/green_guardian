# pages/4_🧩_EcoBot_assistant.py
import streamlit as st
from eco_bot import eco_response


st.set_page_config(page_title="🧩 ÉcoBot – Assistant IA", page_icon="♻️", layout="wide")

st.title("🤖 ÉcoBot – Ton Assistant Écologique 🌱")
st.markdown("""
Bienvenue dans ton assistant IA **ÉcoBot** 🌍  
Pose-lui toutes tes questions sur :
- le **tri des déchets**,  
- la **réduction du plastique**,  
- ou même des **astuces écologiques** pour ton quotidien 💡
""")

user_input = st.text_area("💬 Pose ta question à ÉcoBot :", placeholder="Exemple : comment recycler un pot de yaourt en plastique ?")

if st.button("Envoyer") and user_input:
    with st.spinner("Réflexion en cours... 🌿"):
        response = eco_response(user_input)
    st.success("Réponse d’ÉcoBot :")
    st.write(response)
