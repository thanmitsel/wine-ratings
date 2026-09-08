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
- Dependencies in `requirements.txt`: `streamlit`, `pandas`, `openpyxl`

## How to run

From the project root:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m streamlit run src/app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## Project layout

```
WineWanker/
├── README.md
├── requirements.txt          # Python dependencies
├── data/
│   ├── Wine Ratings.xlsx     # Main ratings data (used by the app)
│   └── wine_youtube_videos.xlsx
├── src/
│   └── app.py                # Streamlit wine picker
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