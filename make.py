from django.core.management.utils import get_random_secret_key

def write_environ():
    django_key = get_random_secret_key()
    with open("./django_sets/.env.dist","w") as file:
        file.write("SECRET_KEY=" + django_key + "\n" + "DEBUG=True")

write_environ()
if __name__ == "__main__":
    pass
