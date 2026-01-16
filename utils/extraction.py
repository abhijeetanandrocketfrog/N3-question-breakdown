from typing import List


def extract_terms(response: dict) -> List[str]:
    extracted = []

    for items in response.get("phrases", {}).values():
        for item in items:
            if item.get("text"):
                extracted.append(item["text"])

    extracted.extend(response.get("unmapped_medical_terms", []))
    return list(dict.fromkeys(extracted))


def extract_eb03_and_unmapped_terms(response: dict) -> List[str]:
    extracted = []

    for item in response.get("phrases", {}).get("EB03", []):
        if item.get("text"):
            extracted.append(item["text"])

    return list(dict.fromkeys(extracted))
