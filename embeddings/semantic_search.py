import pickle
import pandas as pd
import numpy as np
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# LOAD MODEL
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# LOAD DATA
df = pd.read_csv(
    "data/processed/final_faculty_profiles.csv"
)

df = df.fillna("")


# LOAD EMBEDDINGS
with open(
    "data/processed/embeddings.pkl",
    "rb"
) as f:

    embeddings = pickle.load(f)


# CLEAN TEXT
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # REMOVE JUNK
    text = re.sub(
        r"Back to Top",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = text.replace("nan", "")
    text = text.replace("None", "")

    return text.strip()


# NORMALIZE USER QUERY
def normalize_query(query):

    query = query.lower().strip()

    # REMOVE NOISY WORDS
    noise_words = [

        "professor",
        "professors",
        "faculty",
        "suggest",
        "find",
        "search",
        "working",
        "work",
        "research",
        "researching",
        "teaching",
        "under",
        "expert",
        "experts",
        "related",
        "specialized",
        "specialization",
        "who",
        "of",
        "on",
        "in",
        "for",
        "me"
    ]

    for word in noise_words:

        query = re.sub(
            rf"\b{word}\b",
            "",
            query
        )

    # SEMANTIC EXPANSION
    abbreviation_map = {

        "ml":
            "machine learning",

        "dl":
            "deep learning",

        "nlp":
            "natural language processing",

        "cv":
            "computer vision",

        "rl":
            "reinforcement learning",

        "ai":
            "artificial intelligence",

        "iot":
            "internet of things",

        "maths":
            "mathematics",

        "cybersec":
            "cyber security",

        "cybersecurity":
            "cyber security",

        "embedded":
            "embedded systems",

        "blockchain":
            "distributed systems blockchain cryptocurrency",

        "vlsi":
            "very large scale integration hardware systems",

        "english":
            "english literature philosophy humanities",

        "finance":
            "financial engineering economics fintech",

        "robotics":
            "robotics automation control systems",

        "cloud":
            "cloud computing distributed systems",

        "security":
            "cyber security cryptography network security"
    }

    words = query.split()

    expanded_words = []

    for word in words:

        if word in abbreviation_map:

            expanded_words.append(
                abbreviation_map[word]
            )

        else:

            expanded_words.append(word)

    query = " ".join(expanded_words)

    query = re.sub(
        r"\s+",
        " ",
        query
    )

    return query.strip()


# MAIN SEARCH FUNCTION
def search_faculty(query, top_k=6):

    # NORMALIZE QUERY
    query = normalize_query(query)

    # GENERATE QUERY EMBEDDING
    query_embedding = model.encode([query])

    # COSINE SIMILARITY
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # SORT RESULTS
    top_indices = np.argsort(
        similarities
    )[::-1]

    results = []

    for idx in top_indices:

        score = similarities[idx]

        # STRICT FILTER
        if score < 0.23:
            continue

        faculty = df.iloc[idx]

        results.append({

            "name":
                clean_text(
                    faculty.get("name", "")
                ),

            "specialization":
                clean_text(
                    faculty.get(
                        "specialization",
                        ""
                    )
                ),

            "teaching":
                clean_text(
                    faculty.get(
                        "teaching",
                        ""
                    )
                ),

            "biography":
                clean_text(
                    faculty.get(
                        "biography",
                        ""
                    )
                ),

            "email":
                clean_text(
                    faculty.get(
                        "email",
                        ""
                    )
                ),

            "phone":
                clean_text(
                    faculty.get(
                        "phone",
                        ""
                    )
                ),

            "source_url":
                clean_text(
                    faculty.get(
                        "source_url",
                        ""
                    )
                ),

            "score":
                float(score)
        })

        # LIMIT RESULTS
        if len(results) >= top_k:
            break

    return results