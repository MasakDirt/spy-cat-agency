from typing import Callable

import requests
from django.conf import settings

from spy_agency.exceptions import RequestError


def get_cat_breed_names() -> set:
    try:
        response = requests.get(settings.API_URL)
        response.raise_for_status()
        breeds = response.json()
        return {breed['name'].lower() for breed in breeds}
    except requests.exceptions.RequestException as e:
        raise RequestError(f"Error fetching breeds from API: {e}")


def validate_cat_breed(user_breed: str, exception: Callable) -> None:
    breed_names = get_cat_breed_names()
    if not user_breed.lower() in breed_names:
        raise exception(f"Breed {user_breed} not found!")
