"""
Saves channel photos for the YouTube-only creators in photo-checklist.csv,
using the official YouTube Data API (free key, about 40 of the 10,000 daily quota units).

1. Get a free API key: console.cloud.google.com -> new project -> enable "YouTube Data API v3"
   -> Credentials -> Create API key.
2. Run from this folder:   python fetch_youtube_photos.py YOUR_API_KEY
3. Photos are saved here with the checklist's save_as name. Check youtube_matches.csv:
   channels found by name search can occasionally be the wrong channel.
Existing files are skipped, so it is safe to re-run.
"""
import csv, json, os, sys, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3/"
HERE = os.path.dirname(os.path.abspath(__file__))

def call(endpoint, **params):
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)

def find_channel(key, handle_or_name):
    if handle_or_name.startswith("@"):
        items = call("channels", part="snippet,statistics", forHandle=handle_or_name, key=key).get("items", [])
    else:
        hits = call("search", part="snippet", q=handle_or_name, type="channel", maxResults=1, regionCode="IN", key=key).get("items", [])
        if not hits:
            return None
        items = call("channels", part="snippet,statistics", id=hits[0]["snippet"]["channelId"], key=key).get("items", [])
    return items[0] if items else None

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python fetch_youtube_photos.py YOUR_API_KEY")
    key = sys.argv[1]
    rows = list(csv.DictReader(open(os.path.join(HERE, "photo-checklist.csv"), encoding="utf-8-sig")))
    report = []
    for row in rows:
        if row["platform"] != "YouTube":
            continue
        out = os.path.join(HERE, row["save_as"])
        if os.path.exists(out):
            continue
        try:
            ch = find_channel(key, row["handle_or_channel"])
            if not ch:
                report.append([row["name"], row["handle_or_channel"], "", "", "not found"]); continue
            thumbs = ch["snippet"]["thumbnails"]
            url = (thumbs.get("high") or thumbs.get("medium") or thumbs["default"])["url"]
            with urllib.request.urlopen(url, timeout=20) as r, open(out, "wb") as f:
                f.write(r.read())
            subs = ch.get("statistics", {}).get("subscriberCount", "")
            report.append([row["name"], row["handle_or_channel"], ch["snippet"]["title"], subs, "saved"])
            print("saved", row["save_as"], "->", ch["snippet"]["title"])
        except Exception as e:
            report.append([row["name"], row["handle_or_channel"], "", "", f"error: {e}"])
            print("failed", row["name"], e)
    with open(os.path.join(HERE, "youtube_matches.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["creator", "searched_for", "channel_found", "subscribers_now", "result"])
        w.writerows(report)
    print("Done. Check youtube_matches.csv for the channel each photo came from.")

if __name__ == "__main__":
    main()
