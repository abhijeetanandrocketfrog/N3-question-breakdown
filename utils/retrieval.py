import requests
from typing import List, Dict
from utils.config_loader import load_config

_config = load_config()
_retrieval_cfg = _config.get("retrieval", {})

API_URL = _retrieval_cfg["api_url"]
TOP_K = _retrieval_cfg.get("top_k", 3)
TIMEOUT = _retrieval_cfg.get("timeout", 10)


def retrieve_categories(queries: List[str], top_k: int = TOP_K) -> List[Dict]:
    payload = {
        "queries": queries,
        "top_k": top_k
    }

    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=TIMEOUT
    )

    return response.json()


def retrieve_categories(queries: List[str], top_k: int = TOP_K) -> List[Dict]:
    """
    Calls the retrieval API and returns parsed JSON response.
    """
    payload = {
        "queries": queries,
        "top_k": top_k
    }

    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=10
    )

    return response.json()


def add_eb03_categories_from_api(
    eb_filters: List[str],
    api_response: List[Dict]
) -> List[str]:
    """
    Extracts categories from retrieval API response and
    appends them as EB03 filters if not already present.
    """
    existing = set(eb_filters)

    for item in api_response:
        for result in item.get("results", []):
            category = result.get("category")
            if not category:
                continue

            eb_term = f"EB03: {category}"
            if eb_term not in existing:
                eb_filters.append(eb_term)
                existing.add(eb_term)

    return eb_filters
