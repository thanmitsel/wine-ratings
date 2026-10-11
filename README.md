# WineWanker — Wine Picker

A simple [Streamlit](https://streamlit.io/) app that helps you choose a wine from Tom’s ratings spreadsheet. Filter by **name**, **category**, **shop**, **price**, and **rating**, then browse (or download) the matching bottles.

## What it does

- Loads `data/Wine Ratings.xlsx` (116 wines)
- Sidebar filters: name search, category, shop, price range (£), rating, optional “Tom’s Pick only”
- Results table: Name, Category, Shop, Price, Rating, Tom’s Pick, Best For
- Sorted by rating (Class → Pass → Arse), then price
- CSV download of the filtered results
- Reloads automatically when `Wine Ratings.xlsx` is updated

## Requirements

- **Python 3.13** (or another 3.9+ install — the project’s default `python` on this machine is 3.7, which Streamlit does not support)
- Dependencies in `requirements.txt`: `streamlit`, `pandas`, `openpyxl`, `gspread`, `google-auth`, `gspread-dataframe`

## How to run

From the project root:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m streamlit run src/app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## Google Sheets script modes

`src/google_sheets_api.py` is a CLI for the same sheet the app reads. The app only **loads**. Use this script when you need to **upload** a CSV.

From the project root (needs `.streamlit/secrets.toml` with `google_api` and `wine_ratings_sheet_id`):

```powershell
py -3.13 src/google_sheets_api.py --mode upload
py -3.13 src/google_sheets_api.py --mode load
py -3.13 src/google_sheets_api.py --help
```

| Mode | What it does |
|------|----------------|
| `upload` | Reads `data/wine_ratings.csv` and writes the `clean` worksheet |
| `load` | Reads the `clean` worksheet and prints the first rows (default if you omit `--mode`) |

## Streamlit Cloud

The app reads ratings from Google Sheets (`GoogleSheets.load_clean`), not from the Excel file. Secrets stay out of git (`.streamlit/secrets.toml` is gitignored).

1. Push this repo to GitHub, including `src/app.py`, `src/google_sheets_api.py`, and `requirements.txt`.
2. At [share.streamlit.io](https://share.streamlit.io), deploy the repo with **Main file path** `src/app.py`.
3. In **Advanced settings**, pick **Python 3.13** (or 3.12). Do not leave the default if it is 3.14 — installs can fail.
4. In **Secrets**, paste TOML that matches local `.streamlit/secrets.toml`:

```toml
wine_ratings_sheet_id = "YOUR_SPREADSHEET_ID"

[google_api]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "....iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/...."
universe_domain = "googleapis.com"
```

Quote `client_id` and keep `\n` in `private_key`. Share the spreadsheet with the service account `client_email` as Editor, and keep a worksheet named `clean`.

## Project layout

```
WineWanker/
├── README.md
├── requirements.txt          # Python dependencies
├── data/
│   ├── Wine Ratings.xlsx     # Main ratings data (used by the app)
│   └── wine_youtube_videos.xlsx
├── src/
│   ├── app.py                # Streamlit wine picker
│   └── google_sheets_api.py  # CLI: --mode upload | load
└── tom_gibley_pics/          # Thumbnail / reference images (not used by the app yet)
```

## Data columns

| Column       | Use                                      |
|--------------|------------------------------------------|
| Name         | Wine name (searchable)                   |
| Shop         | Where it’s sold                          |
| Price (£)    | Price filter                             |
| Category     | Style / region / grape                   |
| Rating       | Class, Pass, or Arse                     |
| Tom’s Pick   | Yes / No                                 |
| Best For     | Context of the tasting                   |

# Data collection
PNG from youtube are taken that contain the ratings. Then they get through an LLM to convert to excell file. The ratings may sometimes be different so during the data collection they need to be aligned with the available ratings.

Class, Pass, Arse
Tom's Pick/Tom's * -> Class, The Rest -> Pass unless, arse is mentioned or colour coding red
Not Crap, Crap