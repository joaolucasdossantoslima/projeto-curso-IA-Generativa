from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- CONFIGURAÇÕES ---
ARQUIVO_TXT = "conhecimento.txt"

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

print("D., escaneie o QR code...")

WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.ID, "side"))
)

print("Bot de Fluxo Único Iniciado!")

ultima_mensagem_respondida = ""
estado_conversa = 0 

def buscar_no_txt(termo):
    if not os.path.exists(ARQUIVO_TXT):
        return None
    try:
        with open(ARQUIVO_TXT, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha in linhas:
                if termo.lower() in linha.lower():
                    return linha.strip()
        return None
    except:
        return None

def enviar_mensagem(texto):
    try:
        caixa_texto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        caixa_texto.send_keys(texto)
        caixa_texto.send_keys(Keys.ENTER)
        time.sleep(1) # Pequena pausa para garantir o envio
    except Exception as e:
        print(f"Erro ao enviar: {e}")

def responder_mensagem():
    global ultima_mensagem_respondida, estado_conversa
    try: 
        mensagens = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')

        if mensagens:
            texto_recebido = mensagens[-1].text.split('\n')[0].strip().lower()

            if texto_recebido != ultima_mensagem_respondida:
                print(f"Estado {estado_conversa} - Usuário: {texto_recebido}")

                # --- COMANDO GLOBAL PARA VOLTAR ---
                if texto_recebido == "menu inicial":
                    estado_conversa = 0

                # --- LÓGICA DE ESTADOS ---
                
                # ESTADO 0: Manda apenas a Saudação com Menu em UMA bolha
                if estado_conversa == 0:
                    menu_inicial = (
                        "Olá! Eu sou Zar o assistente de montagem de computador."
                        "Como posso ajudar?\n"
                        "1. Montar do zero   "
                        "2. Peças específicas   "
                        "3. Dúvidas   " 
                    )
                    enviar_mensagem(menu_inicial)
                    estado_conversa = 1

                # ESTADO 1: Escolha entre 1, 2 ou 3
                elif estado_conversa == 1:
                    if texto_recebido == "1":
                        menu_uso = (
                            "Ótima escolha! Qual será o uso do PC?\n"
                            "• Escritório  • Trabalho  • Estudo  • Jogos\n"
                            "*(Digite uma das opções acima ou 'Menu Inicial')*"
                        )
                        enviar_mensagem(menu_uso)
                        estado_conversa = 2
                    elif texto_recebido == "2":
                        menu_pecas = (
                            "De qual peça você está procurando informações?\n"
                            "• Fonte  • Memória RAM  • Armazenamento  "
                            "• Processador  • Placa de Vídeo  • Coolers  "
                            "• Periféricos\n"
                            "*(Digite o nome da peça ou 'Menu Inicial')*"
                        )
                        enviar_mensagem(menu_pecas)
                        estado_conversa = 3
                    elif texto_recebido == "3":
                        enviar_mensagem("Função de Dúvidas ainda incompleta.\nDigite 'Menu Inicial' para voltar.")
                    else:
                        enviar_mensagem("Por favor, escolha apenas 1, 2 ou 3.")

                # ESTADO 2: Perfil de Uso
                elif estado_conversa == 2:
                    perfis = ["escritorio", "trabalho", "estudo", "jogos"]
                    if texto_recebido in perfis:
                        res = buscar_no_txt(f"computador {texto_recebido}")
                        msg_final = f"Encontrei esta configuração para {texto_recebido.capitalize()}:\n\n{res}" if res else f"Infelizmente não achei 'computador {texto_recebido}' no meu banco.\n\nTente novamente: Escritório, Trabalho, Estudo ou Jogos."
                        enviar_mensagem(msg_final)
                    else:
                        enviar_mensagem("Opção inválida. Digite Escritório, Trabalho, Estudo ou Jogos.")

                # ESTADO 3: Peças
                elif estado_conversa == 3:
                    pecas = ["fonte", "memoria ram", "armazenamento", "processador", "placa de video", "coolers", "perifericos"]
                    if texto_recebido in pecas:
                        res = buscar_no_txt(texto_recebido)
                        msg_final = f"Informações sobre {texto_recebido.capitalize()}:\n\n{res}" if res else f"Não encontrei informações sobre {texto_recebido} no banco.\n\nEscolha: Fonte, Memória RAM, Armazenamento, Processador, Placa de Vídeo, Coolers ou Periféricos."
                        enviar_mensagem(msg_final)
                    else:
                        enviar_mensagem("Peça não reconhecida. Tente novamente ou digite 'Menu Inicial'.")

                ultima_mensagem_respondida = texto_recebido
    
    except Exception as e:
        pass

# Loop principal
while True:
    responder_mensagem()
    time.sleep(2)