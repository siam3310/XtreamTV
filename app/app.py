import reflex as rx
from app.states.xtream_state import XtreamState
from app.components.navbar import navbar
from app.components.video_player import video_player
from app.components.channel_view import channel_view
from app.components.movies_view import movies_view
from app.components.series_view import series_view


def page_wrapper(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                video_player(),
                class_name="w-full lg:w-[70%] shrink-0 border-r border-white/10 bg-black lg:flex flex-col z-40 order-1",
            ),
            rx.el.main(
                content,
                class_name="flex-1 w-full lg:w-[30%] h-full overflow-y-auto min-h-0 order-2 scroll-smooth bg-zinc-950",
            ),
            class_name="flex-1 flex flex-col lg:flex-row w-full min-h-0 overflow-hidden",
        ),
        class_name="flex flex-col h-screen w-screen bg-black text-white font-mono overflow-hidden",
    )


def index() -> rx.Component:
    return page_wrapper(channel_view())


def movies() -> rx.Component:
    return page_wrapper(movies_view())


def series() -> rx.Component:
    return page_wrapper(series_view())


app = rx.App(
    theme=rx.theme(appearance="light", panel_background="solid"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(href="https://vjs.zencdn.net/8.10.0/video-js.css", rel="stylesheet"),
        rx.el.script(src="https://vjs.zencdn.net/8.10.0/video.min.js"),
    ],
)
app.add_page(index, route="/", on_load=XtreamState.load_data)
app.add_page(movies, route="/movies", on_load=XtreamState.load_data)
app.add_page(series, route="/series", on_load=XtreamState.load_data)