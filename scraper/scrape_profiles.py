# scraper/scrape_profiles.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

links_df = pd.read_csv(
    "data/raw/faculty_links.csv"
)

column_name = links_df.columns[0]

faculty_data = []
failed_urls = []

keywords = [

    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Cyber Security",
    "Cryptography",
    "Data Science",
    "Data Analytics",
    "Big Data",
    "Cloud Computing",
    "IoT",
    "Distributed Systems",
    "Blockchain",
    "Signal Processing",
    "Algorithms",
    "Optimization",
    "Networks",
    "Robotics",
    "Quantum Computing"

]

for url in links_df[column_name]:

    print(f"\nScraping: {url}")

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=40
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # REMOVE JUNK TAGS
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        # NAME
        name = "Unknown Faculty"

        h1 = soup.find("h1")
        h2 = soup.find("h2")

        if h1:
            name = h1.get_text(strip=True)

        elif h2:
            name = h2.get_text(strip=True)

        # EMAIL
        email = ""

        email_patterns = [

            r'[\w\.-]+\s?\[at\]\s?[\w\.-]+\s?\[dot\]\s?[\w\.-]+',

            r'[\w\.-]+@[\w\.-]+\.\w+'
        ]

        for pattern in email_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                email = match.group(0)

                email = (
                    email.replace("[at]", "@")
                    .replace("[dot]", ".")
                    .replace(" ", "")
                )

                break

        # PHONE
        phone = ""

        phone_match = re.search(
            r'0\d{2,4}-\d{6,8}',
            text
        )

        if phone_match:
            phone = phone_match.group(0)

        # SPECIALIZATION
        found_keywords = []

        for keyword in keywords:

            if keyword.lower() in text.lower():
                found_keywords.append(keyword)

        specialization = ", ".join(
            list(set(found_keywords))
        )

        # BIOGRAPHY
        biography = ""

        possible_sections = [

            "Biography",
            "About",
            "Research Interests",
            "Profile"

        ]

        for section in possible_sections:

            pattern = rf'{section}(.*?)(?=Teaching|Courses|Publication|Projects|Awards|Education|Experience|Contact|Phone|Email|$)'

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                biography = match.group(1).strip()

                if len(biography) > 100:
                    break

        biography = re.sub(
            r"\s+",
            " ",
            biography
        ).strip()

        # TEACHING
        teaching = ""

        teach_match = re.search(
            r'Teaching(.*?)(?=Publication|Projects|Awards|Education|Experience|Contact|Phone|Email|$)',
            text,
            re.IGNORECASE
        )

        if teach_match:

            teaching = teach_match.group(1).strip()

        teaching = re.sub(
            r"\s+",
            " ",
            teaching
        ).strip()

        # SEARCH TEXT
        search_text = f"""

Faculty Name:
{name}

Research Interests:
{specialization}

Teaching Subjects:
{teaching}

Faculty Biography:
{biography}

Complete Faculty Profile:
{text}

Possible Domains:
Artificial Intelligence
Machine Learning
Deep Learning
Computer Vision
Natural Language Processing
Cyber Security
Data Science
Big Data Analytics
Networks
Signal Processing
Quantum Computing
Cloud Computing
Distributed Systems
IoT
Blockchain
Robotics

"""

        faculty_data.append({

            "name": name,
            "email": email,
            "phone": phone,
            "specialization": specialization,
            "teaching": teaching,
            "biography": biography,
            "search_text": search_text,
            "source_url": url

        })

        time.sleep(0.5)

    except Exception as e:

        print(f"Error scraping {url}")
        print(e)

        failed_urls.append(url)

# DATAFRAME
df = pd.DataFrame(faculty_data)

# REMOVE DUPLICATES
df.drop_duplicates(
    subset=["name"],
    inplace=True
)

# SAVE
df.to_csv(
    "data/processed/final_faculty_profiles.csv",
    index=False
)

# FAILED URLS
failed_df = pd.DataFrame({
    "failed_url": failed_urls
})

failed_df.to_csv(
    "data/raw/failed_urls.csv",
    index=False
)

print("\nFINAL DATASET CREATED")
print(f"Total Faculty Records: {len(df)}")
print(f"Failed URLs: {len(failed_urls)}")