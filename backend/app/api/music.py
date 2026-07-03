from fastapi import APIRouter
import os
import json

router = APIRouter()


SONGS_DIR = "backend/app/storage/generated/songs"
LYRICS_DIR = "backend/app/storage/generated/lyrics"
METADATA_DIR = "backend/app/storage/generated/metadata"


@router.get("/songs")
def get_songs():

    songs_data = []

    for file in os.listdir(METADATA_DIR):

        if file.endswith(".json"):

            metadata_path = os.path.join(METADATA_DIR, file)

            with open(metadata_path, "r", encoding="utf-8") as f:

                metadata = json.load(f)

                songs_data.append(metadata)

    return songs_data