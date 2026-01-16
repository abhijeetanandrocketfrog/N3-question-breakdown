import re
from typing import List


def sort_eb_filters(eb_filters: List[str]) -> List[str]:
    def key_fn(item: str):
        m = re.match(r"EB(\d+):\s*(.*)", item)
        if not m:
            return (999, item)
        return (int(m.group(1)), m.group(2).lower())

    return sorted(eb_filters, key=key_fn)
