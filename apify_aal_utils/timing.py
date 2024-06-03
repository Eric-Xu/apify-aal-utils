from random import randint
from time import sleep


def add_random_delay(max_seconds: int = 5) -> None:
    random_seconds: int = randint(1, max_seconds)
    print(f"Sleeping for {random_seconds} seconds.")
    sleep(random_seconds)

