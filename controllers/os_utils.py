import os
import sys
import platform
from typing import Union
from string import ascii_lowercase, digits
from random import sample, shuffle


def get_os() -> Union[str]:
    os = platform.system().lower()
    if 'win' in os:
        return 'windows'

    elif any(['linux' in os, 'darwin' in os]):
        return 'linux'

    else:
        sys.exit('Error: system not supported yet')


def gen_folder_name(project_name: str) -> str:
    random_lower = sample(ascii_lowercase, 3)
    random_digits = sample(digits, 3)
    random_comb = [*random_lower, *random_digits]
    shuffle(random_comb)
    random_comb = ''.join(random_comb)
    return f'{project_name}_{random_comb}'
