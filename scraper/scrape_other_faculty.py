import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

pages = {

    "Adjunct Faculty":
    "https://www.daiict.ac.in/adjunct-faculty",

    "International Adjunct Faculty":
    "https://www.daiict.ac.in/adjunct-faculty-international",

    "Distinguished Professor":
    "https://www.daiict.ac.in/distinguished-professor",

    "Professor of Practice":
    "https://www.daiict.ac.in/professor-practice"
}

faculty_data = []

for category, url in pages.items():

    print(f"\nScraping {category}")

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    cards = soup.find_all("div")

    for card in cards:

        card_text = card.get_text(" ", strip=True)

        if len(card_text) < 80:
            continue

        email_match = re.search(
            r'[\w\.-]+\[at\][\w\.-]+\[dot\][\w\.-]+',
            card_text
        )

        if not email_match:
            continue

        email = email_match.group(0)

        email = email.replace("[at]", "@")
        email = email.replace("[dot]", ".")

        lines = card_text.split()

        name = " ".join(lines[:4])

        phone_match = re.search(
            r'0\d{2,4}-\d{6,8}',
            card_text
        )

        phone = (
            phone_match.group(0)
            if phone_match else "Not Available"
        )

        faculty_data.append({

            "name": name,
            "email": email,
            "phone": phone,
            "office": "Not Available",
            "phd": "Not Available",
            "biography": card_text[:500],
            "specialization": card_text[:500],
            "teaching": "Not Available",
            "search_text": card_text,
            "source_url": url
        })

df = pd.DataFrame(faculty_data)

df.drop_duplicates(
    subset=["email"],
    inplace=True
)

df.to_csv(
    "data/processed/other_faculty.csv",
    index=False
)

print("\nOTHER FACULTY DATASET CREATED")
print("Total records:", len(df))