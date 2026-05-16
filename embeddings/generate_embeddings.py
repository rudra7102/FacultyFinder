import pandas as pd
import pickle

from sentence_transformers import SentenceTransformer


# LOAD CSV
df = pd.read_csv(
    "data/processed/final_faculty_profiles.csv"
)

df = df.fillna("")


# CREATE SEMANTIC SEARCH TEXT
df["search_text"] = (

    df["specialization"] + " "

    + df["teaching"] + " "

    + df["biography"]
)


# LOAD MODEL
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# GENERATE EMBEDDINGS
embeddings = model.encode(

    df["search_text"].tolist(),

    show_progress_bar=True
)

# SAVE EMBEDDINGS
with open(
    "data/processed/embeddings.pkl",
    "wb"
) as f:

    pickle.dump(
        embeddings,
        f
    )

print("Embeddings generated successfully.")