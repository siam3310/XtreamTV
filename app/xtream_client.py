import requests
import logging


class XtreamClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_url = f"{self.base_url}/player_api.php"
        self.params = {"username": self.username, "password": self.password}
        self.session = requests.Session()

    def _build_stream_url(
        self, stream_type: str, stream_id: int, extension: str = "ts"
    ) -> str:
        return f"{self.base_url}/{stream_type}/{self.username}/{self.password}/{stream_id}.{extension}"

    def get_categories(self, type_slug: str) -> dict[str, str]:
        try:
            params = self.params.copy()
            params["action"] = type_slug
            response = self.session.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return {
                str(item.get("category_id")): item.get("category_name", "Uncategorized")
                for item in data
            }
        except Exception as e:
            logging.exception(f"Failed to fetch categories ({type_slug}): {e}")
            return {}

    def get_live_streams(self, categories: dict[str, str]) -> list[dict]:
        try:
            params = self.params.copy()
            params["action"] = "get_live_streams"
            response = self.session.get(self.api_url, params=params, timeout=60)
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
                        "id": str(stream_id),
                        "name": item.get("name", "Unknown Channel"),
                        "logo": item.get("stream_icon") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("live", stream_id, "ts"),
                        "type": "live",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch live streams: {e}")
            return []

    def get_vod_streams(self, categories: dict[str, str]) -> list[dict]:
        try:
            params = self.params.copy()
            params["action"] = "get_vod_streams"
            response = self.session.get(self.api_url, params=params, timeout=60)
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
                        "id": str(stream_id),
                        "name": item.get("name", "Unknown Movie"),
                        "logo": item.get("stream_icon") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("movie", stream_id, ext),
                        "type": "movie",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch VOD streams: {e}")
            return []

    def get_series(self, categories: dict[str, str]) -> list[dict]:
        try:
            params = self.params.copy()
            params["action"] = "get_series"
            response = self.session.get(self.api_url, params=params, timeout=60)
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
                        "id": str(series_id),
                        "name": item.get("name", "Unknown Series"),
                        "logo": item.get("cover") or "",
                        "category": categories.get(cat_id, "Uncategorized"),
                        "url": self._build_stream_url("series", series_id, "mp4"),
                        "type": "series",
                    }
                )
            return parsed_items
        except Exception as e:
            logging.exception(f"Failed to fetch series: {e}")
            return []