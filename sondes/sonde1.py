import psutil
import time
import socket

host = socket.gethostname()

epo = int(time.time())
cpu_val = psutil.cpu_percent(interval=1)
ram_val = psutil.virtual_memory().percent

# QUOI ; HOST ; EPO ; VAL
print(f"CPU;{host};{epo};{cpu_val}")
print(f"RAM;{host};{epo};{ram_val}")