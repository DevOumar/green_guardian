# eco_bot.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Charger le modèle et le tokenizer Mistral depuis Hugging Face
model_name = "mistralai/Mistral-7B-Instruct-v0.2"

print("Chargement du modèle Mistral, cela peut prendre un peu de temps...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

print("Modèle chargé avec succès !")

def eco_response(prompt: str) -> str:
    """
    Génère une réponse écologique intelligente à partir du prompt utilisateur.
    """
    messages = [
        {"role": "system", "content": "Tu es ÉcoBot, un assistant expert en recyclage, écologie et tri des déchets."},
        {"role": "user", "content": prompt}
    ]
    text_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    inputs = tokenizer(text_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=250, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
