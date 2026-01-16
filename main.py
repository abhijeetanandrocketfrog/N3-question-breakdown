import json
from utils.eb_filters import extract_eb_filters
from utils.extraction import extract_terms, extract_eb03_and_unmapped_terms
from utils.retrieval import retrieve_categories, add_eb03_categories_from_api
from utils.sorting import sort_eb_filters


if __name__ == "__main__":
    response = {
        "eb_codes": ["EB01", "EB02", "EB03", "EB12"],
        "phrases": {
            "EB02": [{"text": "i", "cluster": "1"}],
            "EB03": [{"text": "hospital outpatient service", "cluster": ["2.3"]}],
            "EB12": [{"text": "in-network", "canonical_term": "In-Plan-Network"}]
        },
        "unmapped_medical_terms": ["approval"]
    }

    # 1. Initial extraction
    output = {
        "eb_filters": extract_eb_filters(response),
        "extracted_terms": extract_terms(response)
    }

    # 2. Terms for retrieval (EB03-only for now)
    retrieval_terms = extract_eb03_and_unmapped_terms(response)

    # 3. Call retrieval API (NOW ABSTRACTED)
    api_response = retrieve_categories(retrieval_terms)

    print("\nAPI Response:")
    print(json.dumps(api_response, indent=2))

    # 4. Update EB filters using API output
    output["eb_filters"] = add_eb03_categories_from_api(
        output["eb_filters"],
        api_response
    )

    # 5. Sort EB filters
    output["eb_filters"] = sort_eb_filters(output["eb_filters"])

    # 6. Final output

    final_output = {
        "Atomic_Questions": [
            {
                "eb_filters": output["eb_filters"],
                "extracted_terms": output["extracted_terms"]
            }
        ]
    }

    print("\nFinal Output:")
    print(json.dumps(final_output, indent=2))
