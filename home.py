from shiny import ui, module

class Home:
    link = lambda text, url: ui.a(text, href = url, target = "_blank", class_ = "link-underline-info")
    links_ = {
        "shiny": link("Shiny for Python", "https://shiny.posit.co/py/"),
        "shinyswatch": link("shinyswatch", "https://posit-dev.github.io/py-shinyswatch/"),
        "bootswatch": link("bootswatch", "https://bootswatch.com/")
    }

@module.ui
def u_i(): return ui.page_fluid(
    ui.h1("Developed with ", Home.links_["shiny"], class_ = "display-1 first"),
    ui.h6("Theme Slate by ", Home.links_["shinyswatch"], " / ", Home.links_["bootswatch"], class_ = "display-6"),
    class_ = "vh-100 d-flex flex-column justify-content-center align-items-center text-center"
)