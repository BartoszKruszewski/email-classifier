import sys

import httpx

URL = "http://localhost:8000/api/v1/route-message"
EMAIL = "jan.kowalski@firma.pl"

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

TEST_CASES = [
    # HELP_DESK
    ("HELP_DESK", "Hej, moja myszka przestała działać. Macie jakieś zapasowe na stanie?"),
    ("HELP_DESK", "Potrzebuję nowy monitor, obecny ma bardzo słaby kontrast."),

    # IT
    ("IT", "Cześć, wyskakuje mi błąd logowania i nie mam dostępu do produkcyjnej bazy danych."),
    ("IT", "VPN ciągle mnie rozłącza po kilku minutach pracy."),

    # KADRY
    ("KADRY", "Dzień dobry, złożyłem zwolnienie lekarskie. Proszę o informację, jak to wpłynie na moje wynagrodzenie."),
    ("KADRY", "Kiedy otrzymam formularz podatkowy PIT-11 za ubiegły rok?"),

    # HR
    ("HR", "Czy firma dofinansowuje kursy językowe lub certyfikaty branżowe?"),
    ("HR", "Na kiedy zaplanowane są nadchodzące roczne oceny pracownicze?"),

    # OTHER
    ("OTHER", "Ta firma jest super :)"),
    ("OTHER", "Ktoś zostawił niebieski parasol w kuchni na drugim piętrze."),
]

all_passed = True

with httpx.Client(timeout=30.0) as client:
    for expected, message in TEST_CASES:
        response = client.post(URL, json={"email": EMAIL, "message": message})
        response.raise_for_status()
        res = response.json()
        actual = res.get("department")

        is_ok = actual == expected
        all_passed = all_passed and is_ok
        status = f"{GREEN}[OK]{RESET}" if is_ok else f"{RED}[FAILED (got '{actual}')]{RESET}"
        print(f"{status} Expected: {expected:<9} | Message: {message}")

sys.exit(0 if all_passed else 1)
