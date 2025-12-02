import reflex as rx
from app.states.xtream_state import XtreamState
from app.components.navbar import navbar
from app.components.video_player import video_player
from app.components.channel_view import channel_view
from app.components.movies_view import movies_view
from app.components.series_view import series_view


def template(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                video_player(),
                class_name="w-full lg:w-[65%] shrink-0 bg-black aspect-video lg:aspect-auto lg:h-full border-r border-white/10",
            ),
            rx.el.div(
                content,
                class_name="flex-1 h-full overflow-y-auto bg-zinc-900 relative scroll-smooth",
                id="content-scroll-area",
            ),
            class_name="flex flex-col lg:flex-row flex-1 overflow-hidden h-[calc(100vh-64px)]",
        ),
        class_name="flex flex-col h-screen bg-black font-sans text-white overflow-hidden font-['Inter']",
    )


def index():
    return template(channel_view())


def movies():
    return template(movies_view())


def series():
    return template(series_view())


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="blue"
    ),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(index, route="/", on_load=XtreamState.load_data)
app.add_page(movies, route="/movies", on_load=XtreamState.load_data)
app.add_page(series, route="/series", on_load=XtreamState.load_data)