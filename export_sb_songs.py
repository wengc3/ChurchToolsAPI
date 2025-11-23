import json
import logging
import logging.config
from pathlib import Path

from churchtools_api.churchtools_api import ChurchToolsApi

logger = logging.getLogger(__name__)

config_file = Path("logging_config.json")
with config_file.open(encoding="utf-8") as f_in:
    logging_config = json.load(f_in)
    log_directory = Path(logging_config["handlers"]["file"]["filename"]).parent
    if not log_directory.exists():
        log_directory.mkdir(parents=True)
    logging.config.dictConfig(config=logging_config)

SB_CATEGORY_ID = 2


if __name__ == '__main__':
    # Prepare output folder
    folder = Path('songs')
    # Create folder if it doesn't exist
    folder.mkdir(parents=True, exist_ok=True)
    # Create Session
    from secure.config_ext import ct_users
    from secure.config_ext import ct_domain
    api = ChurchToolsApi(ct_domain, ct_user='systemusersongs', ct_password=ct_users['systemusersongs'])
    api.login_ct_rest_api
    songs = api.get_songs()
    for song in songs:
      if "(SB" in song["name"]:
        if not song["arrangements"][0]["files"]:
           print(song["name"])
           continue
        filename = song["arrangements"][0]["files"][0]["name"]
        url = song["arrangements"][0]["files"][0]["fileUrl"]
        target_path = folder / filename
        api.file_download_from_url(url, target_path)
    exit(0)