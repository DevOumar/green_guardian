# pages/1_🧠_Analyse_d_image.py
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from model_loader import load_model
import pandas as pd
from datetime import datetime
import os
import uuid
from io import BytesIO

# -----------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------
st.set_page_config(page_title="🧠 Analyse d’image – GreenGuardian", page_icon="🌿", layout="wide")
st.title("🧠 Analyse d’image – Tri Intelligent des Déchets")

# -----------------------------
# CHARGEMENT DU MODÈLE IA
# -----------------------------
with st.spinner("Chargement du modèle IA..."):
    model = load_model()
st.success("✅ Modèle chargé avec succès !")

# Les classes de ton modèle
imagenet_labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# -----------------------------
# CHOIX DE LA MÉTHODE D'IMPORT
# -----------------------------
st.markdown("### 🖼️ Choisis ta méthode d'importation")

if "image_data" not in st.session_state:
    st.session_state.image_data = None

option = st.radio(
    "Sélectionne une option :",
    ("📂 Importer une image", "📷 Prendre une photo"),
    horizontal=True
)

image = None

if option == "📂 Importer une image":
    uploaded_file = st.file_uploader("📸 Téléversez une image de déchet", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.session_state.image_data = uploaded_file.getvalue()
        image = Image.open(uploaded_file)

elif option == "📷 Prendre une photo":
    st.info("👉 Clique ci-dessous pour activer la caméra seulement si tu veux prendre une photo.")
    camera_photo = st.camera_input("Prends une photo du déchet 📷")
    if camera_photo is not None:
        st.session_state.image_data = camera_photo.getvalue()
        image = Image.open(camera_photo)

# Récupérer l'image depuis la session si disponible
if st.session_state.image_data and image is None:
    image = Image.open(BytesIO(st.session_state.image_data))

# -----------------------------
# AFFICHAGE DE L’IMAGE & ANALYSE
# -----------------------------
if image:
    st.image(image, caption="🧾 Image chargée", use_column_width=True)

    if st.button("🔍 Analyser maintenant"):
        with st.spinner("Analyse de l’image en cours..."):
            # Prétraitement
            img = image.resize((224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array[tf.newaxis, ...])

            # Prédiction
            preds = model.predict(img_array)
            top_pred = np.argmax(preds[0])
            confidence = preds[0][top_pred] * 100
            label = imagenet_labels[top_pred]

        # Résultats
        st.subheader(f"🧠 Prédiction : **{label.capitalize()}**")
        st.progress(int(confidence))
        st.write(f"Confiance : **{confidence:.2f}%**")

        # -----------------------------
        # CONSEIL ÉCOLOGIQUE
        # -----------------------------
        eco_tips = {
            "plastic": "🧴 Pense à bien rincer les bouteilles et pots en plastique avant de les jeter ♻️",
            "paper": "📄 Retire les agrafes ou le scotch pour un meilleur recyclage du papier ✂️",
            "metal": "🥫 Écrase les canettes pour gagner de la place et faciliter le tri 💪",
            "glass": "🍾 Jette le verre sans bouchon ni couvercle, et évite la vaisselle 🚫",
            "cardboard": "📦 Aplatis les cartons avant de les jeter, ça optimise le transport 🚛",
            "trash": "🚯 Ce déchet n’est pas recyclable. Essaie de réduire son usage 🌍"
        }

        advice = eco_tips.get(label, "🌱 Continue à trier intelligemment pour préserver la planète 💚")
        st.info(advice)

        # -----------------------------
        # ENREGISTREMENT AUTOMATIQUE
        # -----------------------------
        history_file = "history.csv"
        images_dir = "saved_images"
        os.makedirs(images_dir, exist_ok=True)

        image_filename = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(images_dir, image_filename)
        image.save(image_path)

        new_entry = pd.DataFrame([{
            "image_path": image_path,
            "prediction": label,
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        if not os.path.exists(history_file):
            new_entry.to_csv(history_file, index=False)
        else:
            old_data = pd.read_csv(history_file)
            updated_data = pd.concat([old_data, new_entry], ignore_index=True)
            updated_data.to_csv(history_file, index=False)

        st.success("✅ Résultat sauvegardé dans l’historique !")

        # -----------------------------
        # BOUTON DE CORRECTION
        # -----------------------------
        if st.button("❌ L’IA s’est trompée ?"):
            st.info("Merci pour ton retour ! (fonctionnalité d'apprentissage futur à venir)")
