**Live demo:** https://smartdesk-m56puz9qidv8fhxprsju6z.streamlit.app/

*The demo uses a fictional business and limits messages per session to keep usage costs low.*

![SmartDesk screenshot](docs/screenshot.png)

# SmartDesk: AI Customer Support Assistant

SmartDesk answers customer questions using a business's own documents
(FAQ, price list, policies), sorts each message by category and urgency,
and flags messages that need the owner's attention.

The demo uses a fictional business, *Nakasero Phone Fix*.

## What it does

1. **Reads business documents** from `.txt` files in `business_docs/`.
2. **Answers customer questions** using only those documents. If the answer
   isn't there, it says so and points the customer to the business phone number.
3. **Classifies each message** (question, order, complaint, other) with an
   urgency level (low, medium, high).
4. **Flags messages for the owner** when a human is needed, such as complaints,
   refund disputes and anything not covered by the documents.

## Built with

Python, Google Gemini (`google-genai`), Pydantic (structured output),
Streamlit (web interface).

## How to run it

**You need:** Windows, Python 3 installed, and a Gemini API key from
Google AI Studio.

1. Copy `.env.example` to a new file named `.env`.
2. Open `.env` and fill in your values:
   - `GEMINI_API_KEY`: your API key
   - `GEMINI_MODEL`: a Gemini model name available to your key
   - `BUSINESS_NAME`: the business name shown on the page
3. Double-click `run_smartdesk.bat`. The first run installs what it needs.
4. Your browser opens the SmartDesk page. If Streamlit asks for an email on
   first run, you can press Enter to skip it.

**Manual alternative:**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Using it for a different business

Replace the files in `business_docs/` with that business's own text files and
change `BUSINESS_NAME` in `.env`. No code changes are needed.

## Testing

Run `python test_smartdesk.py`. It sends sample customer messages and checks the results. 
Response times in my tests: 2-4 seconds, measured from Kampala. Speed varies with internet connection and server demand.

## Reliability and safety

- Checks for missing settings or documents and shows a clear message.
- Retries if the AI service is busy, then falls back to flagging the owner.
- Limits message length to 1000 characters.
- The API key stays in `.env`, which is never uploaded to GitHub.

## Limitations

- AI can make mistakes. Complaints and unusual requests are flagged for a human.
- Documents are loaded as plain text, which suits small businesses. Very large
  catalogs would need a different approach.
- It drafts replies but does not send them or change prices or policies.