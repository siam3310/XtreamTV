import reflex as rx
from app.states.xtream_state import XtreamState


def navbar_link(text: str, href: str) -> rx.Component:
    is_active = XtreamState.router.page.path == href
    return rx.el.li(
        rx.el.a(
            text,
            href=href,
            on_click=XtreamState.close_menu,
            class_name=rx.cond(
                is_active,
                "text-sm font-bold text-white bg-white/10 px-4 py-2 rounded-md block lg:bg-transparent lg:p-0 lg:border-b-2 lg:border-white lg:rounded-none",
                "text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 px-4 py-2 rounded-md block transition-colors lg:bg-transparent lg:p-0 lg:hover:bg-transparent",
            ),
        ),
        class_name="w-full lg:w-auto",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1("XtreamTV", class_name="text-xl font-bold tracking-tighter"),
                rx.cond(
                    XtreamState.total_items_loaded > 0,
                    rx.el.span(
                        f"{XtreamState.total_items_loaded} items",
                        class_name="text-xs text-gray-500 font-mono ml-2 hidden sm:block",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.nav(
                rx.el.ul(
                    navbar_link("Live TV", "/"),
                    navbar_link("Movies", "/movies"),
                    navbar_link("Series", "/series"),
                    class_name="hidden lg:flex items-center gap-8",
                )
            ),
            rx.el.button(
                rx.cond(
                    XtreamState.is_menu_open,
                    rx.icon("x", class_name="h-6 w-6 text-white"),
                    rx.icon("menu", class_name="h-6 w-6 text-white"),
                ),
                on_click=XtreamState.toggle_menu,
                class_name="lg:hidden p-2 hover:bg-white/10 rounded-md transition-colors",
            ),
            class_name="flex items-center justify-between w-full h-16",
        ),
        rx.cond(
            XtreamState.is_menu_open,
            rx.el.div(
                rx.el.nav(
                    rx.el.ul(
                        navbar_link("Live TV", "/"),
                        navbar_link("Movies", "/movies"),
                        navbar_link("Series", "/series"),
                        class_name="flex flex-col gap-2 p-4",
                    )
                ),
                class_name="absolute top-16 left-0 right-0 bg-black border-b border-white/10 shadow-xl animate-in slide-in-from-top-2 lg:hidden",
            ),
        ),
        class_name="w-full bg-black border-b border-white/10 px-6 sticky top-0 z-50",
    )