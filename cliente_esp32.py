import network
import time
import urequests
import random

URL_API = "https://juice-wharf-decibel.ngrok-free.dev/api/temperatura"

# Configuração da rede Wi-Fi do Wokwi
SSID = "Wokwi-GUEST"
PASSWORD = ""  # Sem senha para a rede guest

def conecta_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Conectando ao rede Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        
        # Aguarda a conexão se estabelecer
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
            
    print("\nConexão estabelecida com sucesso!")
    print("Configurações de rede (IP, Máscara, Gateway, DNS):", wlan.ifconfig())



def api():
  print("Iniciando o simulador de temperatura:")
  
  while (True):
    try:
      temperatura_simulada = round(random.uniform(22.0, 34.0)) 
      print(f"\nTemperatura atual: {temperatura_simulada}°C")

      dados = { "temperatura": temperatura_simulada }

      print("Enviando dados para a API...")
      resposta= urequests.post(URL_API, json=dados)

      print(f"Código HTTP de resposta: {resposta.status_code}")

      if (resposta.status_code == 200):
        dados_resposta = resposta.json()
        print(f"Resposta do servidor: {dados_resposta}")
        comando = dados_resposta.get("comando",  "NENHUM")
        if (comando == "LIGAR_COOLER"):
          print("-> [AÇÃO ESP32] Ativando cooler virtual!")
        else:
          print("-> [AÇÃO ESP32] Mantendo cooler desligado")
      resposta.close()
    except Exception as e:
        print(f"Erro durante a comunicação: {e}")
    time.sleep(5)

# Executa a função de conexão
conecta_wifi()

api()
