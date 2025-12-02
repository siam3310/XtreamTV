import reflex as rx
from app.utils.xtream_client import XtreamClient
import logging
import asyncio


class XtreamState(rx.State):
    """
    State management for Xtream IPTV data.
    Handles fetching, parsing, categorization, search, and pagination.
    """

    base_url: str = "http://filex.me:8080"
    username: str = "MAS101A"
    password: str = "MAS101AABB"
    displayed_channels: list[dict[str, str]] = []
    displayed_movies: list[dict[str, str]] = []
    displayed_series: list[dict[str, str]] = []
    channel_categories: list[str] = []
    movie_categories: list[str] = []
    series_categories: list[str] = []
    channel_search_query: str = ""
    channel_selected_category: str = "All"
    movie_search_query: str = ""
    movie_selected_category: str = "All"
    series_search_query: str = ""
    series_selected_category: str = "All"
    is_loading: bool = False
    is_limited_load: bool = False
    total_items_loaded: int = 0
    error_message: str = ""
    current_stream_url: str = ""
    current_original_url: str = ""
    current_stream_title: str = ""
    is_menu_open: bool = False
    view_mode: str = "list"
    _all_channels: list[dict[str, str]] = []
    _all_movies: list[dict[str, str]] = []
    _all_series: list[dict[str, str]] = []
    _page_size: int = 20
    _channel_limit: int = 20
    _movie_limit: int = 20
    _series_limit: int = 20

    @rx.event(background=True)
    async def load_data(self):
        """
        Fetches and processes the Xtream Codes data in the background.
        """
        async with self:
            if self.total_items_loaded > 0:
                logging.info("Data already loaded, skipping.")
                return
            logging.info("Starting to load Xtream API data...")
            self.is_loading = True
            self.error_message = ""
            self.displayed_channels = []
            self.displayed_movies = []
            self.displayed_series = []
        try:
            client = XtreamClient(self.base_url, self.username, self.password)
            logging.info("Fetching categories...")
            live_cats, vod_cats, series_cats = await asyncio.gather(
                client.get_categories("get_live_categories"),
                client.get_categories("get_vod_categories"),
                client.get_categories("get_series_categories"),
            )
            logging.info("Fetching streams...")
            channels, movies, series = await asyncio.gather(
                client.get_live_streams(live_cats),
                client.get_vod_streams(vod_cats),
                client.get_series(series_cats),
            )
            logging.info(
                f"Fetch complete. Channels: {len(channels)}, Movies: {len(movies)}, Series: {len(series)}"
            )
            async with self:
                self._all_channels = channels
                self._all_movies = movies
                self._all_series = series
                self.channel_categories = list(dict.fromkeys(live_cats.values()))
                self.movie_categories = list(dict.fromkeys(vod_cats.values()))
                self.series_categories = list(dict.fromkeys(series_cats.values()))
                self.total_items_loaded = len(channels) + len(movies) + len(series)
                self.displayed_channels = self._filter_list(
                    self._all_channels,
                    self.channel_search_query,
                    self.channel_selected_category,
                )[: self._channel_limit]
                self.displayed_movies = self._filter_list(
                    self._all_movies,
                    self.movie_search_query,
                    self.movie_selected_category,
                )[: self._movie_limit]
                self.displayed_series = self._filter_list(
                    self._all_series,
                    self.series_search_query,
                    self.series_selected_category,
                )[: self._series_limit]
                self.is_loading = False
                logging.info("State updated successfully.")
        except Exception as e:
            logging.exception(f"Failed to load data: {e}")
            async with self:
                self.error_message = f"Failed to load content: {str(e)}"
                self.is_loading = False

    @rx.event
    def retry_loading(self):
        return XtreamState.load_data

    @rx.event
    def update_displayed_channels(self):
        filtered = self._filter_list(
            self._all_channels,
            self.channel_search_query,
            self.channel_selected_category,
        )
        self.displayed_channels = filtered[: self._channel_limit]

    @rx.event
    def search_channels(self, query: str):
        self.channel_search_query = query
        self._channel_limit = self._page_size
        self.update_displayed_channels()

    @rx.event
    def filter_channels_by_category(self, category: str):
        self.channel_selected_category = category
        self._channel_limit = self._page_size
        self.update_displayed_channels()

    @rx.event
    def load_more_channels(self):
        self._channel_limit += self._page_size
        self.update_displayed_channels()

    @rx.event
    def reset_channel_filters(self):
        self.channel_search_query = ""
        self.channel_selected_category = "All"
        self._channel_limit = self._page_size
        self.update_displayed_channels()

    @rx.event
    def update_displayed_movies(self):
        filtered = self._filter_list(
            self._all_movies, self.movie_search_query, self.movie_selected_category
        )
        self.displayed_movies = filtered[: self._movie_limit]

    @rx.event
    def search_movies(self, query: str):
        self.movie_search_query = query
        self._movie_limit = self._page_size
        self.update_displayed_movies()

    @rx.event
    def filter_movies_by_category(self, category: str):
        self.movie_selected_category = category
        self._movie_limit = self._page_size
        self.update_displayed_movies()

    @rx.event
    def load_more_movies(self):
        self._movie_limit += self._page_size
        self.update_displayed_movies()

    @rx.event
    def reset_movie_filters(self):
        self.movie_search_query = ""
        self.movie_selected_category = "All"
        self._movie_limit = self._page_size
        self.update_displayed_movies()

    @rx.event
    def update_displayed_series(self):
        filtered = self._filter_list(
            self._all_series, self.series_search_query, self.series_selected_category
        )
        self.displayed_series = filtered[: self._series_limit]

    @rx.event
    def search_series(self, query: str):
        self.series_search_query = query
        self._series_limit = self._page_size
        self.update_displayed_series()

    @rx.event
    def filter_series_by_category(self, category: str):
        self.series_selected_category = category
        self._series_limit = self._page_size
        self.update_displayed_series()

    @rx.event
    def load_more_series(self):
        self._series_limit += self._page_size
        self.update_displayed_series()

    @rx.event
    def reset_series_filters(self):
        self.series_search_query = ""
        self.series_selected_category = "All"
        self._series_limit = self._page_size
        self.update_displayed_series()

    def _filter_list(
        self, items: list[dict[str, str]], query_str: str, category_str: str
    ) -> list[dict[str, str]]:
        """Helper to filter a list by search query and category."""
        result = items
        if category_str and category_str != "All":
            result = [item for item in result if item.get("category") == category_str]
        if query_str:
            query = query_str.lower()
            result = [item for item in result if query in item.get("name", "").lower()]
        return result

    @rx.event
    def play_stream(self, url: str, title: str):
        """Sets the current stream to play, converting .ts to .m3u8 for HLS support."""
        self.current_original_url = url
        if url.endswith(".ts"):
            self.current_stream_url = url.replace(".ts", ".m3u8")
        else:
            self.current_stream_url = url
        self.current_stream_title = title

    @rx.event
    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def close_menu(self):
        self.is_menu_open = False

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode