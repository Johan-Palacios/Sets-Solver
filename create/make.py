import os
import platform
import subprocess

def create_linux_env():
    try:
        os.system('python3.10 -m venv venv')
        os.system('create/activate.sh')
        print("Ejecute python3.10 manage.py runserver")
    except Exception as e:
        print("Ha ocurrido un error")
        raise e

if platform.system() in ["Linux", "Darwin"]:
    create_linux_env()
elif platform.system() == "Windows":
    pass
else:
    print("Plataforma No soportada")
