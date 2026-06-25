from pathlib import Path

from datasets import load_dataset
BASE_DIR = Path(__file__).resolve().parent.parent
output_file  = BASE_DIR / "dataset" / "The_Arabic_E-Book_Corpus.xlsx"
# Load dataset
ds = load_dataset("mohres/The_Arabic_E-Book_Corpus")

# Convert the train split to pandas DataFrame
df = ds["train"].to_pandas()
print(df.columns)
# Save to Excel
df.to_excel(output_file, index=False)

print("Saved successfully!")