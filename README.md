# Creator Finder (local)

Creator discovery for brands and agencies: search a niche, browse Top / Macro / Micro creators, and open a creator to see contacts.

Pages: **Home** (search and tiers), **Own Demo** (load your own roster and photos, at `#own-demo`) and **News** (this week's creator news, at `#news`).

## Run it

**Windows:** double-click `start-website.bat`. Your browser opens **http://localhost:8080**. Keep the black window open while you use the site, and close it to stop.

If it says Python is missing, install it from https://www.python.org/downloads/ (tick "Add python.exe to PATH") and run the file again.

Manual start, from this folder in a terminal:

```
python -m http.server 8080
```

then open http://localhost:8080. With Node.js instead: `npx serve -l 8080 .`

## Folders

| Path | What it is |
|---|---|
| `index.html` | The whole website: layout, styles and code in one file |
| `data/creators.json` | The 298-creator roster the site loads. Edit it to add emails, managers or new creators |
| `data/creators.md` | The same roster as a readable table with sources |
| `data/news.json` | The 10 stories on the News page. Replace them each week and refresh the page |
| `photos/` | Creator photos. Name each file as in `photo-checklist.csv` (for example `Ankur Warikoo @ankurwarikoo.jpg`) and refresh the page |
| `photos/photo-checklist.csv` | Every creator with profile link and the file name to save their photo as |
| `photos/top-creators-photos.csv` | The 70 creators with 1M+ followers |
| `photos/fetch_youtube_photos.py` | Optional: saves the YouTube-only creators' channel photos using a free YouTube Data API key |

## Notes

- Photos in `photos/` and edits to `data/creators.json` or `data/news.json` only show when the site runs on localhost. Opening `index.html` directly still works, with the built-in roster and no folder photos.
- Fonts load from Google Fonts, so the serif headings need an internet connection; without one the site falls back to system fonts.
- Follower counts are snapshots from public rankings (see `data/creators.md` for each source). Contact fields are empty until you add them.
