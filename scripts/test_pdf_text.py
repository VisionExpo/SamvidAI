from pathlib import Path
import fitz  # PyMuPDF

PDF_PATH = Path("data/govt_contracts/BARC_General_Conditions_of_Contract_GCC.pdf")

def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at {PDF_PATH.resolve()}")

    doc = fitz.open(PDF_PATH)
    print(f"[INFO] Total pages: {len(doc)}")

    text = doc[0].get_text()
    print("\n----- SAMPLE TEXT (PAGE 1) -----\n")
    print(text[:1500])

if __name__ == "__main__":
    main()
