from shiny import ui, module, render, reactive
from utils import ShinyDF
import pandas as pd, pokebase as pb

class Pokedex(ShinyDF):
    df_ = pb.APIResourceList("pokemon")
    df_ = pd.DataFrame({"Name": list(df_.names)}, index = [i + 1 for i in range(df_.count)])
    df_ = df_.assign(
        Sprite = df_.index.map(lambda i: pb.SpriteResource("pokemon", i).url if i <= 1025 else pd.NA),
        Artwork = df_.index.map(lambda i: pb.SpriteResource("pokemon", i, other = True, official_artwork = True).url if i <= 1025 else pd.NA)
    )

    types_ = {
        "normal": "gray",
        "fighting": "orange",
        "flying": "skyblue",
        "poison": "purple",
        "ground": "sandybrown",
        "rock": "brown",
        "bug": "lightgreen",
        "ghost": "slateblue",
        "steel": "darkgray",
        "fire": "red",
        "water": "blue",
        "grass": "green",
        "electric": "yellow",
        "psychic": "pink",
        "ice": "lightblue",
        "dragon": "darkslateblue",
        "dark": "black",
        "fairy": "lightpink",
    }

    choices = {
        "types": {i + 1: t for i, t in enumerate(types_.keys())},
        "moves": {i + 1: m for i, m in enumerate(pb.APIResourceList("move").names)},
        "gens": [pb.generation(i + 1) for i in range(len(pb.APIResourceList("generation")))]
    }

    choices["gens"] = {
        i + 1: "Generation {} ({})".format(i + 1, " ".join([v.name for vg in g.version_groups for v in vg.versions]))
        for i, g in enumerate(choices["gens"])
    }

    generation_ = {}

    @staticmethod
    def fetch_ids(from_: str, idx: tuple):
        idx = (int(i) for i in idx)
        match from_:
            case "types": return [p.pokemon.id_ for t in idx for p in pb.type_(t).pokemon]
            case "moves": return [p.id_ for m in idx for p in pb.move(m).learned_by_pokemon]
            case _: return idx

    @staticmethod
    def fetch(id: int):
        p = pb.pokemon(id)
        return {
            "Number": p.id_,
            "Name": p.name,
            "Type": [p.types[i].type.name for i in range(len(p.types))],
            "HP": p.stats[0].base_stat,
            "Attack": p.stats[1].base_stat,
            "Defense": p.stats[2].base_stat,
            "Special Attack": p.stats[3].base_stat,
            "Special Defense": p.stats[4].base_stat,
            "Speed": p.stats[5].base_stat,
        }
    
    @classmethod
    def sprite(self, id: int): return ui.popover(
        ui.img(src = self.get("Sprite")[id]),
        ui.img(src = self.get("Artwork")[id], class_ = "img-fluid")
    )

    def __init__(self, filters: dict = {}):
        if not len(filters): return super().__init__(pd.DataFrame())

        ids = [id for ep, idx in filters.items() for id in self.fetch_ids(ep, idx)]
        ids = [int(id) for id in ids if id in self.generation_]

        pokemon = pd.DataFrame([self.fetch(id) for id in ids]).set_index("Number")
        super().__init__(pokemon)

    def display(self):
        dt = self.df.assign(
            Name = [ui.span(self.sprite(i), ui.br(), n) for i, n in self.df["Name"].items()],
            Type = [ui.div(*[ui.p(t, style = f"color:{self.types_[t]}") for t in pt]) for pt in self.df["Type"]]
        )
        return self.data_table(dt)
    
    def pie(self):
        if self.df.empty: return None
        types = pd.Series([t for ts in self.df["Type"] for t in ts])
        types = types.groupby(types).count()
        colors = [self.types_[t] for t in types.index]
        return types.plot.pie(
            y = 0,
            autopct = "%1.1f%%",
            colors = colors,
            textprops = {"color": "white"}
        )

@module.ui
def u_i(): return ui.page_fluid(
    ui.h1("Pokémon", class_ = "first"),
    ui.input_select("generation", label = None, choices = Pokedex.choices["gens"], width = "50%"),
    ui.row(
        ui.input_selectize("numbers", "Number:", Pokedex.get("Index").to_list(), multiple = True),
        ui.input_selectize("names", "Name:", Pokedex.get("Name").to_dict(), multiple = True),
        ui.input_selectize("moves", "Move:", Pokedex.choices["moves"], multiple = True),
    ),
    ui.input_checkbox_group("types", "Type:", Pokedex.choices["types"], inline = True),
    ui.output_data_frame("pokedex"),
    ui.output_plot("type_stats"),
    # ui.output_plot("battle_stats")
)

@module.server
def server(input, output, session):
    inputs = ["numbers", "names", "types", "moves"]

    @reactive.effect
    @reactive.event(input.generation)
    def _():
        gen_ids = {p.id_: p.name for p in pb.generation(int(input.generation())).pokemon_species}
        Pokedex.set(generation = dict(sorted(gen_ids.items())))
        ui.update_selectize("numbers", choices = [*Pokedex.get("generation").keys()])
        ui.update_selectize("names", choices = Pokedex.get("generation"))

    px_ = reactive.value(Pokedex())

    @output
    @render.data_frame
    def pokedex():
        px = Pokedex({i: input[i]() for i in inputs if input[i]()})
        if px.df.empty: return px.df
        px_.set(px)
        return px.display()

    @output
    @render.plot(transparent = True)
    def type_stats(): return px_.get().pie()