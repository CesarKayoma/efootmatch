
import time
import urllib.request
import urllib.error
from datetime import datetime

# COLOQUE A URL DO SEU SITE AQUI
URL = "https://efootmatch.onrender.com/"

# Intervalo entre requisições (10 minutos)
INTERVALO = 10 * 60


def ping():
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        requisicao = urllib.request.Request(
            URL,
            headers={"User-Agent": "SiteKeepAlive/1.0"}
        )

        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            print(f"[{horario}] ONLINE - HTTP {resposta.status}")

    except Exception as erro:
        print(f"[{horario}] ERRO - {erro}")


print(f"Monitorando: {URL}")
print("Intervalo: 10 minutos")
print("Pressione CTRL+C para encerrar.\n")

try:
    while True:
        ping()
        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")
