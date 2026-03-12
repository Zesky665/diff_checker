# Deployment Guide

## Local Testing

Run the application locally:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deploying to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (https://share.streamlit.io)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: ZIP file comparison tool"
   git push
   ```

2. **Deploy on Streamlit Community Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Click "Deploy"

### Files Required
- `app.py` - Main Streamlit application
- `zip_comparator.py` - Comparison logic module
- `requirements.txt` - Python dependencies

## Features

- Upload two ZIP files via browser
- Compare file and directory structures
- View unique files in each ZIP
- See common files
- Display total file/directory counts

## Limitations
- Maximum file size: 200MB per file (Streamlit Cloud limit)
- Files are processed in memory, not permanently stored
