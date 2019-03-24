import random
import string


ENV_FILE = '.env'
SECRET_KEY_FORMAT = '!!{}!!'


def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def set_secret(path, secret_key, value=None, secret_length=32):
    value = value or generate_key(secret_length)
    with open(path, 'r+') as f:
        content = f.read().replace(SECRET_KEY_FORMAT.format(secret_key), value)
        f.seek(0)
        f.write(content)
        f.truncate()


def set_secrets(path):
    set_secret(path, 'POSTGRES_USER')
    set_secret(path, 'POSTGRES_PASSWORD')


def main():
    set_secrets(ENV_FILE)


if __name__ == '__main__':
    main()