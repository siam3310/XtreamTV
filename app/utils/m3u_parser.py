import requests
import re
import logging


class M3UParser:
    @staticmethod
    def parse_m3u(url: str, max_items: int = 25000) -> list[dict[str, str]]:
        """
        Fetches and parses an M3U playlist from a URL using streaming to save memory.
        Returns a list of dictionaries containing channel/content info.
        Limits parsing to max_items to prevent OOM on huge playlists.
        """
        logging.info(f"Fetching M3U playlist from: {url} (Limit: {max_items})")
        parsed_items = []
        try:
            with requests.get(url, stream=True, timeout=90) as response:
                response.raise_for_status()
                attr_pattern = re.compile('([a-zA-Z0-9-]+)="([^"]*)"')
                current_item = {}
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        line_str = line.decode("utf-8", errors="ignore").strip()
                    except Exception as e:
                        logging.exception(f"Error decoding line: {e}")
                        continue
                    if not line_str:
                        continue
                    if line_str.startswith("#EXTINF"):
                        attributes = dict(attr_pattern.findall(line_str))
                        current_item = {
                            "name": "",
                            "logo": attributes.get("tvg-logo", ""),
                            "category": attributes.get("group-title", "Uncategorized"),
                            "url": "",
                            "tvg_id": attributes.get("tvg-id", ""),
                        }
                        last_comma_index = line_str.rfind(",")
                        if last_comma_index != -1:
                            current_item["name"] = line_str[
                                last_comma_index + 1 :
                            ].strip()
                        else:
                            current_item["name"] = attributes.get(
                                "tvg-name", "Unknown Channel"
                            )
                    elif line_str.startswith("http") and current_item:
                        current_item["url"] = line_str
                        parsed_items.append(current_item)
                        current_item = {}
                        if len(parsed_items) >= max_items:
                            logging.info(
                                f"Hit limit of {max_items} items. Stopping parse."
                            )
                            break
        except Exception as e:
            logging.exception(f"Error parsing M3U stream: {e}")
            raise e
        logging.info(f"Successfully parsed {len(parsed_items)} items.")
        return parsed_items