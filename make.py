from django.core.management.utils import get_random_secret_key

def write_environ():
    django_key = get_random_secret_key()
    with open("./.env.dist","w") as file:
        file.write("SECRET_KEY=" + django_key + "\n" + "DEBUG=True")

if __name__ == "__main__":
    write_environ()
