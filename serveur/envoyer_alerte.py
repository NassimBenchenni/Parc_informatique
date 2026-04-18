import smtplib
from email.mime.text import MIMEText
import sys
import os
from dotenv import load_dotenv

# 1. On force Python à lire le fichier .env
load_dotenv()

EMAIL_ADDRESS = os.environ.get("GMAIL_EMAIL")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASS")

machine = sys.argv[1]
message = sys.argv[2]

with open("template_mail.txt", "r", encoding="utf-8") as f:
    texte = f.read().replace("__MACHINE__", machine).replace("__MESSAGE__", message)

msg = MIMEText(texte)
msg['Subject'] = f"ALERTE - Monitoring ({machine})"
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS    

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
    server.send_message(msg)
    server.quit()
    print(f"-> Email d'alerte envoyé via Gmail à {msg['To']}")
except Exception as e:
    print(f"Erreur lors de l'envoi Gmail : {e}")