import logging
import re
import os

from churchtools_api.churchtools_api import ChurchToolsApi

SB_SOURCE_ID = 2
CATEGORY_ID = 0
SNG_SOURCE_FOLDER = "D:\\Daten\\Eigene Dokumente\\SongBeamer\\Songs\\SB"
EXCLUDED_SONGS = [1,2,3,4,56,425,323,430,221,432,349,115]
ARRANGEMENT_NAME = "Standard-Arrangement"

def _get_songs_from_sng(folder_path):
    """Get all .sng files from the specified folder."""
    songs = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.sng'):
            song_title = file_name.replace(".sng", "")
            # Extract the SB number first
            sb_match = re.search(r'\(SB\s*(\d+)\)', song_title)
            sb_number = sb_match.group(1).lstrip('0') if sb_match else None
            # Handle edge case where number is all zeros
            if sb_number == '':
                sb_number = '0'
            # Remove patterns like (SB 001), (SB001), etc.
            song_title = re.sub(r'\s*\(SB\s*\d+\)\s*', '', song_title).strip()
            songs.append({
                'file_path': os.path.join(folder_path, file_name),
                'title': song_title,
                'sb_number': sb_number
            })
    return songs

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    # Create Session
    from secure.config import ct_token
    from secure.config import ct_domain
    api = ChurchToolsApi(ct_domain, ct_token=ct_token)

    # get songs from sng files from Songbeamer folder SB
    songs = _get_songs_from_sng(SNG_SOURCE_FOLDER)
    
    # for each file create new song in churchtools
    for song in songs:
        if song['sb_number'] is None or int(song['sb_number']) in EXCLUDED_SONGS:
            logging.info(f"Skipping song '{song['title']}' with SB number '{song['sb_number']}'")
            continue

        logging.info(f"Processing song '{song['title']}' with SB number '{song['sb_number']}'")

        
        new_song = api.create_song_rest(title=song['title'],songcategory_id=CATEGORY_ID)
        if not new_song:
            logging.error(f"Failed to create song '{song['title']}'")
            continue 
        logging.info(f"Created new song '{new_song['name']}' with ID {new_song['id']}")
        arrangement = api.create_song_arrangement_rest(
            song_id=new_song['id'],
            arrangement_name=ARRANGEMENT_NAME,
            source_id=SB_SOURCE_ID,
            source_ref=song['sb_number']
        )
        if not arrangement:
            logging.error(f"Failed to create arrangement for song ID {new_song['id']}")
            continue
        is_default = api.set_song_arrangement_as_default(
            song_id=new_song['id'],
            arrangement_id=arrangement['id']
        )
        if not is_default:
            logging.error(f"Failed to set arrangement ID {arrangement['id']} as default for song ID {new_song['id']}")
            continue
        file = api.file_upload(song['file_path'], domain_type='song_arrangement', domain_identifier=arrangement['id'])
        if not file:
            logging.error(f"Failed to upload file for arrangement ID {arrangement['id']}")
            continue
        logging.info(f"Uploaded file '{os.path.basename(song['file_path'])}' to arrangement ID {arrangement['id']}")    


    
