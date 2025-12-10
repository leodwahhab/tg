from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(
    title="API Próximo Trem ViaMobilidade (usando API oficial)",
    version="2.1"
)

# ===============================
# DICIONÁRIO CÓDIGO → NOME REAL
# ===============================

ESTACOES = {
    "VAG": "Varginha",
    "MVN": "Bruno Covas - Mendes - Vila Natal",
    "GRA": "Grajaú",
    "INT": "Primavera - Interlagos",
    "AUT": "Autódromo",
    "JUR": "Jurubatuba - Senac",
    "SOC": "Socorro",
    "SAM": "Santo Amaro",
    "GJT": "Granja Julieta",
    "MRB": "Morumbi - Claro",
    "BRR": "Berrini",
    "VOL": "Vila Olímpia",
    "CJD": "Cidade Jardim",
    "HBR": "Hebraica - Rebouças",
    "PIN": "Pinheiros",
    "USP": "Cidade Universitária",
    "JAG": "Villa Lobos - Jaguaré",
    "CEA": "Ceasa",
    "JOD": "João Dias",
    "PAL": "Presidente Altino",
    "OSA": "Osasco",
    "JPR": "Júlio Prestes",
    "BFU": "Palmeiras - Barra Funda",
    "LAB": "Lapa",
    "DMO": "Domingos de Moraes",
    "ILE": "Imperatriz Leopoldina",
    "CSA": "Comandante Sampaio",
    "QTU": "Quitaúna",
    "GMC": "General Miguel Costa",
    "CPB": "Carapicuíba",
    "STE": "Santa Terezinha",
    "AJO": "Antonio João",
    "BRU": "Barueri",
    "JBE": "Jardim Belval",
    "JSI": "Jardim Silveira",
    "JDI": "Jandira",
    "SCO": "Sagrado Coração",
    "ECD": "Engenheiro Cardoso",
    "IPV": "Itapevi",
    "SRT": "Santa Rita",
    "AMB": "Ambuitá",
    "ABU": "Amador Bueno"
}

# =========================================
# LINHAS → APENAS LISTA DOS CÓDIGOS
# =========================================

LINHAS = {
    "L8": ["JPR", "BFU", "LAB", "DMO", "ILE", "PAL", "OSA", "CSA",
           "QTU", "GMC", "CPB", "STE", "AJO", "BRU", "JBE", "JSI",
           "JDI", "SCO", "ECD", "IPV", "SRT", "AMB", "ABU"],

    "L9": ["VAG", "MVN", "GRA", "INT", "AUT", "JUR", "SOC", "SAM",
           "GJT", "MRB", "BRR", "VOL", "CJD", "HBR", "PIN", "USP",
           "JAG", "CEA", "JOD", "PAL", "OSA"]
}

API_BASE = "https://apim-proximotrem-prd-brazilsouth-001.azure-api.net/api/v1"


def get_next_train(linha: str, estacao: str):
    url = f"{API_BASE}/lines/{linha}/stations/{estacao}/next-train"

    headers = {"User-Agent": "MyApp/1.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na requisição para API Próximo Trem: {str(e)}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"API retornou status {resp.status_code}: {resp.text}"
        )

    try:
        return resp.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Resposta da API Próximo Trem não é JSON válido")


