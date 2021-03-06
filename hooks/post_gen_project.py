import random
import string
import subprocess
from subprocess import check_call, check_output, CalledProcessError

ENV_FILE = '.env'
SECRET_KEY_FORMAT = '!!{}!!'
DEFAULT_KEY_CHARS = string.ascii_letters + string.digits


def generate_key(length, chars=DEFAULT_KEY_CHARS):
    return ''.join(random.choice(chars) for _ in range(length))


def set_secret(path, secret_key, value=None, secret_length=32, chars=DEFAULT_KEY_CHARS):
    value = value or generate_key(secret_length, chars)
    with open(path, 'r+') as f:
        content = f.read().replace(SECRET_KEY_FORMAT.format(secret_key), value)
        f.seek(0)
        f.write(content)
        f.truncate()


def set_secrets(path):
    set_secret(path, 'POSTGRES_USER')
    set_secret(path, 'POSTGRES_PASSWORD')
    set_secret(path, 'SECRET_KEY', secret_length=50,
               chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')


def main():
    set_secrets(ENV_FILE)
    check_call(['git', 'init'])
    try:
        check_output(['git', 'rev-list', '--count', 'HEAD'], stderr=subprocess.DEVNULL)
    except CalledProcessError:
        check_call(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])
    print('[?] For add a remote repo: git remote add origin <repo>')
    print('[?] Push to remote origin: git push origin master')


if __name__ == '__main__':
    main()
