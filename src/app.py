import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOGS_PATH = BASE_DIR / "logs.csv"
USERS_PATH = BASE_DIR / "users.json"
SUSPICIOUS_IPS_PATH = BASE_DIR / "suspicious_ips.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


def load_csv(path):
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_json(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as file:
        return json.load(file)


logs_df = load_csv(LOGS_PATH)
users = load_json(USERS_PATH, {})
suspicious_ips_data = load_json(SUSPICIOUS_IPS_PATH, {"ips": []})
suspicious_ips = suspicious_ips_data.get("ips", [])


def analyze_log(log):
    risk = "baixo"
    reasons = []

    user = log.get("user")
    attempts = log.get("attempts", 0)
    location = log.get("location")
    ip = log.get("ip")
    time_str = str(log.get("time", ""))

    if attempts >= 3:
        risk = "alto"
        reasons.append("Multiplas tentativas de login")

    if user in users:
        expected_location = users[user].get("location")
        if location != expected_location:
            risk = "alto"
            reasons.append("Localizacao incomum")

    if ip in suspicious_ips:
        risk = "alto"
        reasons.append("IP suspeito")

    try:
        hour = int(time_str.split(":")[0])
        if hour < 6 or hour >= 23:
            if risk != "alto":
                risk = "medio"
            reasons.append("Horario incomum")
    except (ValueError, IndexError):
        if risk == "baixo":
            risk = "medio"
        reasons.append("Horario invalido no log")

    if not reasons:
        reasons.append("Comportamento normal")

    return risk, reasons


def generate_ai_response(log, risk, reasons):
    prompt = f"""
Analise este evento de seguranca.

Log: {log}
Risco: {risk}
Motivos: {reasons}

Responda de forma curta com:
1. problema identificado
2. nivel de risco
3. recomendacao pratica
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        if not response.ok:
            return f"Erro Ollama {response.status_code}: {response.text}"

        data = response.json()
        return data.get("response", "Erro: a API nao retornou o campo 'response'.")
    except requests.RequestException as exc:
        return f"Erro ao consultar a IA local: {exc}"
    except ValueError:
        return "Erro: a API retornou uma resposta que nao e JSON valido."


st.set_page_config(page_title="Agente IA de Seguranca", layout="centered")

st.title("Agente IA de Seguranca")
st.write("Analise um log de acesso e veja o risco identificado.")

user = st.text_input("Usuario", "gabriel")
ip = st.text_input("IP", "185.220.101.45")
location = st.text_input("Localizacao", "Russia")
time = st.text_input("Horario", "03:12")
action = st.text_input("Acao", "login_failed")
attempts = st.number_input("Tentativas", min_value=0, value=5, step=1)

if st.button("Analisar"):
    log = {
        "user": user,
        "ip": ip,
        "location": location,
        "time": time,
        "action": action,
        "attempts": attempts,
    }

    risk, reasons = analyze_log(log)
    ai_response = generate_ai_response(log, risk, reasons)

    st.subheader("Resultado")
    st.write(f"**Risco:** {risk}")
    st.write(f"**Motivos:** {', '.join(reasons)}")

    st.subheader("Resposta da IA")
    st.write(ai_response)
