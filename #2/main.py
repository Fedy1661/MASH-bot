import subprocess
import threading

threading.Thread(target=subprocess.run, args=['py vk_bot.py']).start()
threading.Thread(target=subprocess.run, args=['py telegram_bot.py']).start()
