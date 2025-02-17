from shiny import ui, module, reactive, render
import httpx, re, matplotlib, pandas as pd
from utils import ShinyDF

class Trunk(ShinyDF):
    api_ = {
        "url": "https://db.ygoprodeck.com/api/v7/cardinfo.php",
        "headers": {"User-Agent": "Chrome/51.0.2704.103"}
    }

    cols_ = {
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

    filters_ = ["search" if k == "name" else k for k in list(cols_.keys())[:-1] if k != "desc"]

    frames_ = {
        "effect": "#F5A623",
        "fusion": "#A98BEF",
        "link": "#1B4F91",
        "normal": "#FDE68A",
        "pendulum": "#1DB954",
        "ritual": "#5AB4E5",
        "spell": "#4CAF50",
        "synchro": "#F2F2F2",
        "trap": "#8E44AD",
        "xyz": "#1E1E1E",
    }

    @classmethod
    @reactive.extended_task
    async def fetch(self):
        client = httpx.AsyncClient()
        cards = await client.get(self.api_["url"], headers = self.api_["headers"])
        await client.aclose()
        cards = cards.json()["data"]
        cards = pd.json_normalize(cards).set_index("id")
        cards = cards[~cards["frameType"].isin(["skill", "token"])]
        cards = cards.rename(columns = self.cols_)[self.cols_.values()]
        cards = cards.assign(
            Frame = ["pendulum" if "pendulum" in f else f for f in cards["Frame"]],
            Level = [int(lvl) if not pd.isna(lvl) else pd.NA for lvl in cards["Level"]],
            Thumbnail = [img[0]["image_url_cropped"] for img in cards["img"]],
            Card = [{"md": img[0]["image_url_small"], "lg": img[0]["image_url"]} for img in cards["img"]]
        )
        return cards.drop(columns = "img")

    @classmethod
    def pie(self, index: pd.Index):
        frames = self.df_.loc[index].groupby("Frame").count().iloc[:, :1]
        colors = [self.frames_[f] for f in frames.index]
        return frames.plot.pie(
            y = 0,
            autopct = "%1.1f%%",
            colors = colors,
            textprops = {"color": "white"}
        )

    @classmethod
    def bar(self, index: pd.Index):
        cards = self.df_.loc[index].set_index("Name")[["Attack", "Defense"]]
        colors = matplotlib.colors.ListedColormap(["FireBrick", "Gray"])
        return cards.plot.bar(rot = 0, colormap = colors)

    def __init__(self, filters: dict):
        if not len(filters): return super().__init__(pd.DataFrame())
        super().__init__(self.df_.drop(columns = ["Thumbnail", "Card"]))

        for filter, input in filters.items():
            match filter:
                case "search": self.search(input)
                case "frameType":
                    frames = "|".join(input)
                    frames = [f for f in self.df_["Frame"] if re.search(frames, f)]
                    self.query(f"{self.cols_[filter]} in {frames}")
                case "level":
                    levels = [int(lvl) for lvl in input]
                    self.query(f"{self.cols_[filter]} in {levels}")
                case "atk": self.query(f"{self.cols_[filter]} <= {input}")
                case "def": self.query(f"{self.cols_[filter]} <= {input}")
                case _: self.query(f"{self.cols_[filter]} in {input}")

        self.query()
    
    def search(self, search: str):
        self.df = self.df[
            self.df["Name"].str.contains(search, case = False) |
            self.df["Description"].str.contains(search, case = False)
        ]
        return self
    
    def thumbnail(self, c_id: int): return ui.popover(
        ui.img(src = self.df_["Thumbnail"][c_id], class_ = "w-50 h-50 img-fluid img-thumbnail"),
        ui.img(src = self.df_["Card"][c_id]["lg"], height = "600px")
    )
    
    def display(self):
        dt = self.df.assign(
            Name = [ui.span(self.thumbnail(i), ui.br(), n) for i, n in self.df["Name"].items()],
            Description = [ui.popover("...", d) for d in self.df["Description"]]
        )
        return self.data_table(dt)

@module.ui
def u_i(): return ui.page_fluid(
    ui.h1("Yu-Gi-Oh!", class_ = "first"),
    ui.input_text("search", "Search:", width = "50%"),
    ui.row(
        ui.input_selectize("archetype", "Archetype:",
            choices = [],
            multiple = True
        ),
        ui.input_selectize("race", "Type:",
            choices = [],
            multiple = True
        )
    ),
    ui.row(
        ui.input_checkbox_group("frameType", "Frame:", choices = []),
        ui.input_checkbox_group("attribute", "Attribute:", choices = [])
    ),
    ui.input_checkbox_group("level", "Level:", choices = []),
    ui.row(
        ui.input_slider("atk", "Attack:", min = 0, max = 5000, value = 0),
        ui.input_slider("def", "Defense:", min = 0, max = 5000, value = 0),
    ),
    ui.output_data_frame("trunk"),
    ui.output_text("cards"),
    ui.output_plot("stats")
)

@module.server
def server(input, output, session):
    inputs_ = Trunk.get("filters")

    @reactive.effect
    def _():
        Trunk.fetch()
        trunk = Trunk.fetch.result()

        ui.update_selectize("archetype", choices = trunk["Archetype"].dropna().sort_values().to_list())
        ui.update_selectize("race", choices = trunk["Type"].dropna().sort_values().to_list())
        ui.update_checkbox_group("frameType",
            choices = trunk["Frame"].dropna().to_list(),
            inline = True
        )
        ui.update_checkbox_group("attribute",
            choices = trunk["Attribute"].dropna().to_list(),
            inline = True
        )

        levels = range(trunk["Level"].min(), trunk["Level"].max() + 1)
        ui.update_checkbox_group("level", choices = list(levels), inline = True)

        ui.update_slider("atk", max = trunk["Attack"].max())
        ui.update_slider("def", max = trunk["Defense"].max())

        Trunk.df_ = trunk

    @output
    @render.data_frame
    def trunk():
        trunk = Trunk({i: input[i]() for i in inputs_ if input[i]()})
        return trunk.display() if not trunk.df.empty else trunk.df
    
    @reactive.calc
    def selected(): return trunk.data_view(selected = True)
    
    @output
    @render.text
    def cards():
        n = selected().shape[0]
        if n == 1: return "Card"
        elif n in range(2, 39): return "Combo"
        elif n in range(40, 60): return "Deck"
        else: return ""

    @output
    @render.plot(transparent = True)
    def stats():
        cards = selected()
        if cards.empty: return None
        if not cards["Frame"].str.match("spell|trap").any(): return Trunk.bar(cards.index)
        else: return Trunk.pie(cards.index)
