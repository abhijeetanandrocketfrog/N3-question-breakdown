import requests
from typing import List, Dict
from utils.config_loader import load_config

_config = load_config()
_retrieval_cfg = _config.get("retrieval", {})

TOP_K = 15
API_URL = _retrieval_cfg["api_url"]
TIMEOUT = _retrieval_cfg.get("timeout", 10)
DESIRED_TOP_K = _retrieval_cfg.get("desired_top_k", 3)
SIMILARITY_THRESHOLD = _retrieval_cfg.get("similarity_threshold", 0.85)

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
    Adds up to desired_new_k NEW EB03 filters
    whose similarity score >= similarity_threshold.
    """
    existing = set(eb_filters)
    new_added = 0

    for item in api_response:
        for result in item.get("results", []):
            if new_added >= DESIRED_TOP_K:
                return eb_filters

            score = result.get("score", 0)
            category = result.get("category")

            if not category:
                continue

            # Apply threshold
            if score < SIMILARITY_THRESHOLD:
                continue

            eb_term = f"EB03: {category}"

            # Skip duplicates
            if eb_term in existing:
                continue

            eb_filters.append(eb_term)
            existing.add(eb_term)
            new_added += 1

    return eb_filters