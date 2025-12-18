# Quick Start Guide

Get up and running with the Challenge Annotator in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Your Synapse Token

1. Create your secrets file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Get your Synapse Personal Access Token:
   - Go to https://www.synapse.org/
   - Settings → Personal Access Tokens → Create New Token
   - Select scopes: `view`, `download`, `modify`

3. Add your token to `.streamlit/secrets.toml`:
   ```toml
   SYNAPSE_AUTH_TOKEN = "paste-your-token-here"
   ```

## Step 3: Run the App

```bash
streamlit run app.py
```

The app will open automatically at http://localhost:8501

## Step 4: Start Annotating

1. Select a project from the sidebar
2. Browse Wiki pages or folders
3. Fill out the annotation form
4. Click "Update Annotations"

That's it! You're ready to go. 🎉

## Need Help?

See the full [README.md](README.md) for detailed documentation.
