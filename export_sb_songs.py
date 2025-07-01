from churchtools_api.churchtools_api import ChurchToolsApi
from pathlib import Path

SB_CATEGORY_ID = 1
DOMAIN_ID = 77


if __name__ == '__main__':
    # Prepare output folder
    folder = Path('songs')
    # Create folder if it doesn't exist
    folder.mkdir(parents=True, exist_ok=True)
    # Create Session
    from secure.config import ct_token
    from secure.config import ct_domain
    api = ChurchToolsApi(ct_domain, ct_token=ct_token)
    songs = api.get_songs()
    for song in songs:
      if song["category"]["id"] == SB_CATEGORY_ID:
        filename = song["arrangements"][0]["files"][0]["name"]
        url = song["arrangements"][0]["files"][0]["fileUrl"]
        target_path = folder / filename
        api.file_download_from_url(url, target_path)
    exit(0)