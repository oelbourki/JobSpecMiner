# JobMiner Web App

A Streamlit web application that extracts structured information from job descriptions using Google's Gemini AI.

## Features

- 🔍 **AI-Powered Extraction**: Uses Google Gemini API to extract structured information
- 📝 **Easy Input**: Simple interface to paste job descriptions
- 📊 **Structured Output**: View extracted information in organized sections
- 📥 **Download Options**: Download results as TXT or JSON files
- 🔒 **Secure**: API keys stored locally in session, never sent to servers

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter API Key**: Input your Google Gemini API key (stored locally in session)
2. **Paste Job Description**: Copy and paste the job description text
3. **Extract**: Click "Extract Information" button
4. **View Results**: Browse the extracted information in expandable sections
5. **Download**: Download results as TXT or JSON files

## Project Structure

```
JobMiner/
├── app.py                 # Main Streamlit application
├── src/
│   ├── models.py          # Pydantic data models
│   ├── job_extractor.py   # Core extraction logic
│   └── file_generator.py  # File generation utilities
├── utils/
│   └── validators.py      # Input validation
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── requirements.txt       # Python dependencies
```

## Deployment to Streamlit Community Cloud

### Step 1: Push to GitHub

1. Create a new repository on GitHub (or use existing)
2. Push this code to the repository:
   ```bash
   git add .
   git commit -m "Add Streamlit web app"
   git push
   ```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Deploy"

Your app will be available at: `https://your-app-name.streamlit.app`

## Security Notes

- **API Keys**: Your Gemini API key is stored in Streamlit's session state (server-side) and is never exposed to the client or logged
- **No Data Storage**: Job descriptions and extracted data are not stored on our servers
- **HTTPS**: Streamlit Cloud automatically provides HTTPS encryption

## Requirements

- `streamlit>=1.28.0`
- `google-genai>=0.2.0`
- `pydantic>=2.0.0`

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
