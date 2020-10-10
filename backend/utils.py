import random
import string


def create_lobby_code():
    # TODO: Make sure there are no bad words here
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(4))