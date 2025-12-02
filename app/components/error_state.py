import reflex as rx


def error_view(message: str, on_retry: rx.event.EventHandler) -> rx.Component:
    return rx.el.div(
        rx.icon("triangle-alert", class_name="h-12 w-12 text-red-500 mb-4"),
        rx.el.h3(
            "Something went wrong", class_name="text-lg font-bold text-white mb-2"
        ),
        rx.el.p(message, class_name="text-gray-400 text-center max-w-md mb-6"),
        rx.el.button(
            rx.el.span("Try Again"),
            rx.icon("rotate-cw", class_name="h-4 w-4 ml-2"),
            on_click=on_retry,
            class_name="flex items-center px-6 py-2 bg-white text-black font-bold rounded-lg hover:bg-gray-200 transition-colors",
        ),
        class_name="w-full py-20 flex flex-col items-center justify-center",
    )