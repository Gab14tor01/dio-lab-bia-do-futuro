import json
from pathlib import Path

import pandas as pd
import requests

print("main1 iniciou")

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

print("arquivos carregados")


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


if __name__ == "__main__":
    print("inicio do script")

    test_log = {
        "user": "gabriel",
        "ip": "185.220.101.45",
        "location": "Russia",
        "time": "03:12",
        "action": "login_failed",
        "attempts": 5,
    }

    print("antes do analyze_log")
    risk, reasons = analyze_log(test_log)

    print("depois do analyze_log")
    print("antes do generate_ai_response")
    ai_response = generate_ai_response(test_log, risk, reasons)

    print("depois do generate_ai_response")
    print("Modelo Ollama:", OLLAMA_MODEL)
    print("Risco:", risk)
    print("Motivos:", reasons)
    print("\nIA:\n", ai_response)

