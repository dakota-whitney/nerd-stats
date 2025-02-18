import requests, pandas as pd
from utils import dir_, excel_

ygo = {
    "api": "https://db.ygoprodeck.com/api/v7/cardinfo.php",

    "cols": {
        "name": "Name",
        "archetype": "Archetype",
        "frameType": "Frame",
        "attribute": "Attribute",
        "race": "Type",
        "desc": "Description",
        "level": "Level",
        "atk": "Attack",
        "def": "Defense",
        "card_images": "img"
    }
}

def update_data():
    cards = requests.get(ygo["api"]).json()["data"]
    cards = pd.json_normalize(cards).set_index("id")
    cards = cards[~cards["frameType"].isin(["skill", "token"])]
    cards = cards.rename(columns = ygo["cols"])[ygo["cols"].values()]
    cards = cards.assign(
        Frame = ["pendulum" if "pendulum" in f else f for f in cards["Frame"]],
        Level = [int(lvl) if not pd.isna(lvl) else pd.NA for lvl in cards["Level"]],
        thumbnail = [img[0]["image_url_cropped"] for img in cards["img"]],
        img_sm = [img[0]["image_url_small"] for img in cards["img"]],
        img_md = [img[0]["image_url"] for img in cards["img"]]
    )
    cards.drop(columns = "img", inplace = True)
    cards.to_excel(excel_, sheet_name = "ygo")

