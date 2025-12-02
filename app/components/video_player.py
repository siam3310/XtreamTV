import reflex as rx
from app.states.xtream_state import XtreamState


def videojs_script(url: str) -> rx.Component:
    """
    Script to initialize and dispose VideoJS player.
    We use a key-based approach where changing the key (url) re-mounts the component,
    triggering the script again.
    """
    return rx.el.script(
        f"\n        (function() {{\n            var videoElement = document.getElementById('video-js-player');\n            if (videoElement) {{\n                if (window.videojs) {{\n                     // Dispose existing player if it exists to prevent memory leaks and conflicts\n                    var oldPlayer = videojs('video-js-player');\n                    if (oldPlayer) {{\n                        oldPlayer.dispose();\n                    }}\n                    \n                    // Re-create the video element since dispose removes it from DOM\n                    // This part is tricky in React/Reflex as DOM is managed by them.\n                    // Instead, we trust Reflex to re-render the video tag when key changes.\n                    \n                    // Wait for the new video tag to be available\n                    setTimeout(function() {{\n                        var newVideoElement = document.getElementById('video-js-player');\n                        if (newVideoElement) {{\n                            var player = videojs(newVideoElement, {{\n                                fluid: true,\n                                controls: true,\n                                autoplay: true,\n                                preload: 'auto',\n                                sources: [{{ src: '{url}', type: 'application/x-mpegURL' }}]\n                            }});\n                            player.play().catch(function(e) {{\n                                console.log('Autoplay prevented:', e);\n                            }});\n                        }}\n                    }}, 100);\n                }}\n            }}\n        }})();\n        "
    )


def video_player() -> rx.Component:
    return rx.el.div(
        rx.cond(
            XtreamState.current_stream_url != "",
            rx.el.div(
                rx.fragment(
                    rx.el.div(
                        rx.el.video(
                            id="video-js-player",
                            class_name="video-js vjs-big-play-centered vjs-theme-fantasy",
                            controls=True,
                            preload="auto",
                            width="100%",
                            height="100%",
                        ),
                        videojs_script(XtreamState.current_stream_url),
                        class_name="w-full h-full",
                    )
                ),
                class_name="relative w-full h-full flex flex-col",
                key=XtreamState.current_stream_url,
            ),
            rx.el.div(
                rx.icon("play", class_name="h-12 w-12 text-gray-700 mb-4"),
                rx.el.p(
                    "Select a channel to start streaming",
                    class_name="text-gray-500 font-medium",
                ),
                class_name="w-full h-full flex flex-col items-center justify-center bg-zinc-900/50",
            ),
        ),
        class_name="w-full h-full bg-black overflow-hidden relative shadow-2xl",
    )