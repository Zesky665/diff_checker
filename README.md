# ZIP File Comparison Tool

A Streamlit application to compare the contents and structure of two ZIP files.

## Features

- Upload and compare two ZIP files
- View unique files in each ZIP
- Display common files
- Show directory structure differences
- File and directory count summaries

## Usage

### Local Development
```bash
pip install -r requirements.txt
streamlit run app.py --server.headless true --server.port 8501 &
```

### Cloud Deployment
See `DEPLOYMENT.md` for Streamlit Community Cloud deployment instructions.

## Project Structure

- `app.py` - Main Streamlit application
- `zip_comparator.py` - ZIP comparison logic
- `requirements.txt` - Python dependencies
- `DEPLOYMENT.md` - Deployment guide