from pathlib import Path
from config import get_setting


def find_setup_problems():
    problems = []
    if not get_setting("GEMINI_API_KEY"):
        problems.append("GEMINI_API_KEY is missing from the settings.")
    if not get_setting("GEMINI_MODEL"):
        problems.append("GEMINI_MODEL is missing from the settings.")
    if not list(Path("business_docs").glob("*.txt")):
        problems.append("No .txt files were found in the business_docs folder.")
    return problems