import requests
import logging
import asyncio


class XtreamClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_url = f"{self.base_url}/player_api.php"
        self.params = {"username": self.username, "password": self.password}

    def _build_stream_url(
        self, stream_type: str, stream_id: int, extension: str = "ts"
    ) -> str:
        """
        Constructs the playback URL for a stream.
        stream_type: 'live', 'movie', or 'series'
        """
        return f"{self.base_url}/{stream_type}/{self.username}/{self.password}/{stream_id}.{extension}"

    async def get_categories(self, type_slug: str) -> dict[str, str]:
        """
        Fetches categories and returns a dict mapping category_id to category_name.
        type_slug: 'get_live_categories', 'get_vod_categories', 'get_series_categories'
        """
        try:
            params = self.params.copy()
            params["action"] = type_slug
            response = await asyncio.to_thread(
                requests.get, self.api_url, params=params, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return {
                str(item.get("category_id")): item.get("category_name", "Uncategorized")
                for item in data
            }
        except Exception as e:
            logging.exception(f"Failed to fetch categories ({type_slug}): {e}")
            return {}

    async def get_live_streams(self, categories: dict[str, str]) -> list[dict]:
        """
        Fetches live streams and maps them to the app's format.
        """
        try:
            params = self.params.copy()
            params["action"] = "get_live_streams"
            response = await asyncio.to_thread(
                requests.get, self.api_url, params=params, timeout=60
            )
            response.raise_for_status()
            data = response.json()
            parsed_items = []
            for item in data:
                cat_id = str(item.get("category_id", ""))
                stream_id = item.get("stream_id")
                if not stream_id:
                    continue
                parsed_items.append(
                    {
                        "name": item.get("name", "Unknown Channel"),
                        "logo": item.get("stream_icon") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("live", stream_id, "ts"),
                        "stream_id": str(stream_id),
                        "type": "live",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch live streams: {e}")
            return []

    async def get_vod_streams(self, categories: dict[str, str]) -> list[dict]:
        """
        Fetches movies (VOD) and maps them to the app's format.
        """
        try:
            params = self.params.copy()
            params["action"] = "get_vod_streams"
            response = await asyncio.to_thread(
                requests.get, self.api_url, params=params, timeout=60
            )
            response.raise_for_status()
            data = response.json()
            parsed_items = []
            for item in data:
                cat_id = str(item.get("category_id", ""))
                stream_id = item.get("stream_id")
                ext = item.get("container_extension", "mp4")
                if not stream_id:
                    continue
                parsed_items.append(
                    {
                        "name": item.get("name", "Unknown Movie"),
                        "logo": item.get("stream_icon") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("movie", stream_id, ext),
                        "stream_id": str(stream_id),
                        "type": "movie",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch VOD streams: {e}")
            return []

    async def get_series(self, categories: dict[str, str]) -> list[dict]:
        """
        Fetches series list and maps them.
        Note: Series usually don't have a direct stream URL without fetching episodes.
        We will map the basic info so they appear in the UI.
        """
        try:
            params = self.params.copy()
            params["action"] = "get_series"
            response = await asyncio.to_thread(
                requests.get, self.api_url, params=params, timeout=60
            )
            response.raise_for_status()
            data = response.json()
            parsed_items = []
            for item in data:
                cat_id = str(item.get("category_id", ""))
                series_id = item.get("series_id")
                if not series_id:
                    continue
                parsed_items.append(
                    {
                        "name": item.get("name", "Unknown Series"),
                        "logo": item.get("cover") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("series", series_id, "mp4"),
                        "stream_id": str(series_id),
                        "type": "series",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch series: {e}")
            return []