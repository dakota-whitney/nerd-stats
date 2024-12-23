from shiny import App, ui
from shinyswatch import theme
from pathlib import Path
import home, ygo, pkmn

app_ui = ui.page_navbar(
    ui.head_content(ui.include_css(Path(__file__).parent / "global.css")),
    ui.nav_spacer(),  # Push the navbar items to the right
    ui.nav_panel("Home", home.u_i("home")),
    ui.nav_panel("Yu-Gi-Oh!", ygo.u_i("ygo")),
    ui.nav_panel("Pokémon", pkmn.u_i("pkmn")),
    title = "NerdStats",
    theme = theme.slate,
    position = "fixed-top",
)

def server(input, output, session):
    ygo.server("ygo")
    pkmn.server("pkmn")

app = App(app_ui, server)