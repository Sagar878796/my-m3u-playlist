import requests
from pathlib import Path

INPUT_FILE = "playlists.txt"
OUTPUT_FILE = "Combined.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

seen = set()
channels = []

def download_playlist(url):
    try:
        print("Downloading:", url)

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        r.raise_for_status()

        return r.text.splitlines()

    except Exception as e:
        print("FAILED:", url)
        print("ERROR:", e)
        return []


def parse_m3u(lines):

    result = []
    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if line.startswith("#EXTINF"):

            block = [line]
            i += 1

            while i < len(lines):

                current = lines[i].strip()

                if not current:
                    i += 1
                    continue

                block.append(current)

                if not current.startswith("#"):

                    stream_url = current

                    if stream_url not in seen:

                        seen.add(stream_url)
                        result.extend(block)

                    break

                i += 1

        else:
            i += 1

    return result


def main():

    playlist_file = Path(INPUT_FILE)

    if not playlist_file.exists():
        print("playlists.txt not found!")
        return

    urls = []

    for line in playlist_file.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if line and not line.startswith("#"):
            urls.append(line)

    print("Total playlists:", len(urls))

    for url in urls:

        lines = download_playlist(url)

        if lines:
            channels.extend(parse_m3u(lines))

    output = ["#EXTM3U"]
    output.extend(channels)

    Path(OUTPUT_FILE).write_text(
        "\n".join(output) + "\n",
        encoding="utf-8"
    )

    print()
    print("==============================")
    print("MERGE COMPLETED")
    print("==============================")
    print("Playlists :", len(urls))
    print("Channels  :", len(seen))
    print("Output    :", OUTPUT_FILE)
    print("==============================")


if __name__ == "__main__":
    main()
