import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

faculty_pages = [

    "https://www.daiict.ac.in/faculty",
    "https://www.daiict.ac.in/adjunct-faculty",
    "https://www.daiict.ac.in/distinguished-professor",
    "https://www.daiict.ac.in/professor-practice"

]

all_links = []

for page in faculty_pages:

    print(f"\nFetching: {page}")

    success = False

    # RETRY 5 TIMES
    for attempt in range(5):

        try:

            response = requests.get(
                page,
                headers=headers,
                timeout=60
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            anchors = soup.find_all("a")

            for a in anchors:

                href = a.get("href")

                if not href:
                    continue

                href = href.strip()

                # FIX RELATIVE LINKS
                if href.startswith("/"):

                    href = (
                        "https://www.daiict.ac.in"
                        + href
                    )

                # KEEP ONLY FACULTY PROFILE LINKS
                if "/faculty/" in href:

                    # REMOVE CATEGORY PAGES
                    bad_links = [

                        "adjunct-faculty",
                        "distinguished-professor",
                        "professor-practice"

                    ]

                    skip = False

                    for bad in bad_links:

                        if href.endswith(bad):

                            skip = True
                            break

                    if not skip:

                        all_links.append(href)

            success = True

            print(f"Success: {page}")

            break

        except Exception as e:

            print(f"Attempt {attempt + 1} failed")
            print(e)

            time.sleep(5)

    if not success:

        print(f"Skipping page: {page}")

# REMOVE DUPLICATES
all_links = list(set(all_links))

# SAVE CSV
df = pd.DataFrame({
    "url": all_links
})

df.to_csv(
    "data/raw/faculty_links.csv",
    index=False
)

print("\nFaculty links saved")
print(f"Total Links: {len(df)}")