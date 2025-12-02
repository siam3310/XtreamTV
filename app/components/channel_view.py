import reflex as rx
from app.states.xtream_state import XtreamState
from app.components.card import media_card
from app.components.error_state import error_view


def channel_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500",
                ),
                rx.el.input(
                    placeholder="Search channels...",
                    on_change=XtreamState.search_channels.debounce(500),
                    class_name="w-full bg-zinc-900 text-white text-sm rounded-lg pl-10 pr-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-white/20 placeholder:text-gray-600",
                ),
                class_name="relative w-full sm:w-72 flex-shrink-0",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("All Categories", value="All"),
                    rx.foreach(
                        XtreamState.channel_categories,
                        lambda c: rx.el.option(c, value=c),
                    ),
                    value=XtreamState.channel_selected_category,
                    on_change=XtreamState.filter_channels_by_category,
                    class_name="w-full sm:w-64 bg-zinc-900 text-white text-sm rounded-lg px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-white/20 border-r-8 border-r-transparent cursor-pointer",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("layout-grid", class_name="h-5 w-5"),
                        on_click=lambda: XtreamState.set_view_mode("grid"),
                        class_name=rx.cond(
                            XtreamState.view_mode == "grid",
                            "p-2.5 rounded-lg bg-white/10 text-white",
                            "p-2.5 rounded-lg text-gray-500 hover:text-white hover:bg-white/5",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("list", class_name="h-5 w-5"),
                        on_click=lambda: XtreamState.set_view_mode("list"),
                        class_name=rx.cond(
                            XtreamState.view_mode == "list",
                            "p-2.5 rounded-lg bg-white/10 text-white",
                            "p-2.5 rounded-lg text-gray-500 hover:text-white hover:bg-white/5",
                        ),
                    ),
                    class_name="flex items-center gap-1 border-l border-white/10 pl-4 ml-2",
                ),
                class_name="flex-1 flex items-center gap-2",
            ),
            class_name="flex flex-col sm:flex-row gap-4 p-4 sticky top-0 z-30 bg-black/95 backdrop-blur-sm border-b border-white/10",
        ),
        rx.cond(
            XtreamState.error_message != "",
            error_view(XtreamState.error_message, XtreamState.retry_loading),
            rx.cond(
                XtreamState.is_loading,
                rx.el.div(
                    rx.el.div(
                        class_name="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-white"
                    ),
                    class_name="w-full h-40 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.cond(
                        XtreamState.displayed_channels.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                XtreamState.displayed_channels,
                                lambda c: media_card(c, "tv-2"),
                            ),
                            class_name=rx.cond(
                                XtreamState.view_mode == "list",
                                "flex flex-col gap-2 px-4",
                                "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-2 xl:grid-cols-3 gap-3 px-4",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "No channels found", class_name="text-gray-500 text-sm"
                            ),
                            class_name="w-full py-12 text-center",
                        ),
                    ),
                    rx.cond(
                        XtreamState.displayed_channels.length() > 0,
                        rx.el.div(
                            rx.el.button(
                                "Load More Channels",
                                on_click=XtreamState.load_more_channels,
                                class_name="px-6 py-3 text-sm font-medium text-gray-400 hover:text-white hover:bg-zinc-900 border border-zinc-800 rounded-lg transition-all mt-8",
                            ),
                            rx.cond(
                                XtreamState.is_limited_load,
                                rx.el.p(
                                    "Playlist partially loaded (25k limit) for performance.",
                                    class_name="text-xs text-gray-600 mt-4 text-center",
                                ),
                            ),
                            class_name="flex flex-col items-center justify-center w-full pb-12",
                        ),
                        rx.el.div(),
                    ),
                    class_name="w-full",
                ),
            ),
        ),
        class_name="flex flex-col w-full",
    )