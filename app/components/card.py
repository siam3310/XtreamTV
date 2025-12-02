import reflex as rx
from app.states.xtream_state import XtreamState


def media_card(item: dict[str, str], icon_type: str = "tv-2") -> rx.Component:
    is_active = XtreamState.current_original_url == item["url"]
    is_poster = (item["type"] == "movie") | (item["type"] == "series")
    aspect_ratio_class = rx.cond(is_poster, "aspect-[2/3]", "aspect-video")
    grid_view = rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    item["logo"] != "",
                    rx.el.img(
                        src=item["logo"],
                        alt=item["name"],
                        loading="lazy",
                        class_name="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-300",
                    ),
                    rx.el.div(
                        rx.icon(icon_type, class_name="h-10 w-10 text-gray-700"),
                        class_name="w-full h-full flex items-center justify-center bg-zinc-900",
                    ),
                ),
                rx.cond(
                    is_active,
                    rx.el.div(
                        rx.icon("play", class_name="h-8 w-8 text-black fill-black"),
                        class_name="absolute inset-0 flex items-center justify-center bg-white/20 backdrop-blur-[1px]",
                    ),
                ),
                class_name=f"{aspect_ratio_class} w-full bg-zinc-900 rounded-md mb-3 overflow-hidden relative shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    item["name"],
                    class_name=rx.cond(
                        is_active,
                        "text-sm font-bold text-white truncate text-left",
                        "text-sm font-medium text-gray-300 truncate group-hover:text-white transition-colors text-left",
                    ),
                ),
                rx.el.p(
                    item["category"],
                    class_name="text-xs text-gray-500 truncate text-left mt-0.5",
                ),
                class_name="w-full",
            ),
            class_name="flex flex-col w-full",
        ),
        on_click=lambda: XtreamState.play_stream(item["url"], item["name"]),
        class_name=rx.cond(
            is_active,
            "group flex flex-col p-3 rounded-xl bg-zinc-800/80 ring-1 ring-white/20 transition-colors duration-200",
            "group flex flex-col p-3 rounded-xl hover:bg-zinc-900/50 transition-colors duration-200",
        ),
    )
    list_view = rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    item["logo"] != "",
                    rx.el.img(
                        src=item["logo"],
                        alt=item["name"],
                        loading="lazy",
                        class_name="w-full h-full object-cover rounded-sm",
                    ),
                    rx.el.div(
                        rx.icon(icon_type, class_name="h-4 w-4 text-gray-600"),
                        class_name="w-full h-full flex items-center justify-center bg-zinc-900 rounded-sm",
                    ),
                ),
                class_name=rx.cond(
                    is_poster,
                    "h-16 w-10 shrink-0 bg-zinc-900 mr-3",
                    "h-12 w-20 shrink-0 bg-zinc-900 mr-3",
                ),
            ),
            rx.el.div(
                rx.el.h3(
                    item["name"],
                    class_name=rx.cond(
                        is_active,
                        "text-sm font-bold text-white text-left line-clamp-1",
                        "text-sm font-medium text-gray-300 group-hover:text-white transition-colors text-left line-clamp-1",
                    ),
                ),
                rx.el.p(
                    item["category"],
                    class_name="text-xs text-gray-500 text-left mt-0.5 line-clamp-1",
                ),
                class_name="flex-1 min-w-0 flex flex-col justify-center",
            ),
            rx.cond(
                is_active,
                rx.el.div(
                    rx.icon("play", class_name="h-4 w-4 text-white"), class_name="ml-2"
                ),
            ),
            class_name="flex flex-row items-center w-full h-full",
        ),
        on_click=lambda: XtreamState.play_stream(item["url"], item["name"]),
        class_name=rx.cond(
            is_active,
            "group w-full p-2 rounded-lg bg-zinc-800 ring-1 ring-white/10 transition-all duration-200",
            "group w-full p-2 rounded-lg hover:bg-zinc-900 transition-all duration-200",
        ),
    )
    return rx.cond(XtreamState.view_mode == "list", list_view, grid_view)