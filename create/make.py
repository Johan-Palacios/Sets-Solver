import os
import platform
from django.core.management.utils import get_random_secret_key

option = int(input("1.Crear entorno virtual\n2.Instalar dependencias\n--> "))


def create_env(command: str):
    try:
        print("Creando entorno virtual")
        os.system(command)
        print("Ejecute source ./venv/bin/activate o venv\\Scripts\\activate.bat(Windows)")
    except Exception as e:
        print("Ha ocurrido un error")
        raise e


def install_dependences(command: str):
    try:
        print("Instalando dependencias")
        os.system(command)
    except Exception as e:
        print("No es posible instalar las dependencias")
        raise e


def create_windows_env():
    try:
        print("Creando entorno virtual")
        os.system("python.exe -m venv venv")
        print("Ejecute venv\\Scripts\\activate.bat")
    except Exception as e:
        print("Ha ocurrido un error")
        raise e


def set_command(venv: str, install: str):
    if option == 1:
        create_env(venv)
    elif option == 2:
        install_dependences(install)
    else:
        invalid()

def write_environ():
    django_key = get_random_secret_key()
    with open("../django_sets/.env","w") as file:
        file.write("SECRET_KEY=" + django_key + "\n" + "DEBUG=FALSE")

def invalid():
    print("Invalid option")


def build():
    if platform.system() in ["Linux", "Darwin"]:
        set_command(
            "python3 -m venv venv", "python3 -m pip install -r requirements.txt"
        )
    elif platform.system() == "Windows":
        set_command(
            "python.exe -m venv venv", "python.exe -m pip install -r requirements.txt"
        )
    else:
        print("Plataforma No soportada")


if __name__ == "__main__":
    build()
