import json
from typing import List, Dict, Any

CLUSTER_DIR = "clusters"
MAPPING_DIR = "mapping"


def load_cluster_file(eb_code: str) -> Dict[str, Any]:
    with open(f"{CLUSTER_DIR}/{eb_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_eb_mappings(eb_code: str) -> Dict[str, List[str]]:
    with open(f"{MAPPING_DIR}/{eb_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def find_cluster_terms(cluster_data: dict, target_id) -> List[str]:
    target_id = str(target_id).strip()
    results = []

    for cluster_id, cluster in cluster_data.items():
        cluster_id = str(cluster_id).strip()

        if cluster_id == target_id:
            if "subclusters" in cluster:
                for sub in cluster.get("subclusters", {}).values():
                    results.extend(sub.get("canonical_terms", []))
                return results
            if "canonical_terms" in cluster:
                return cluster.get("canonical_terms", [])
            return []

        for sub_id, sub in cluster.get("subclusters", {}).items():
            if str(sub_id).strip() == target_id:
                return sub.get("canonical_terms", [])

    return results


def extract_eb_filters(response: dict) -> List[str]:
    eb_filters = []
    phrases = response.get("phrases", {})

    cluster_cache = {}
    mapping_cache = {}

    for eb_code, items in phrases.items():
        for item in items:

            if "canonical_term" in item:
                canonical = item["canonical_term"]

                if eb_code not in mapping_cache:
                    try:
                        mapping_cache[eb_code] = load_eb_mappings(eb_code)
                    except FileNotFoundError:
                        mapping_cache[eb_code] = {}

                expanded = mapping_cache[eb_code].get(canonical, [canonical])
                for term in expanded:
                    eb_filters.append(f"{eb_code}: {term}")
                continue

            if "cluster" in item:
                cluster_ids = item["cluster"]
                if not isinstance(cluster_ids, list):
                    cluster_ids = [cluster_ids]

                if eb_code not in cluster_cache:
                    try:
                        cluster_cache[eb_code] = load_cluster_file(eb_code)
                    except FileNotFoundError:
                        continue

                for cid in cluster_ids:
                    for term in find_cluster_terms(cluster_cache[eb_code], cid):
                        eb_filters.append(f"{eb_code}: {term}")

    return list(dict.fromkeys(eb_filters))
