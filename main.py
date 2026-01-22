import json
from utils.eb_filters import extract_eb_filters, ensure_default_eb03
from utils.extraction import extract_terms, extract_eb03_and_unmapped_terms
from utils.retrieval import retrieve_categories, add_eb03_categories_from_api
from utils.sorting import sort_eb_filters


if __name__ == "__main__":
    response = {
        "eb_codes": ["EB01", "EB02", "EB12"],
        "phrases": {
            "EB01": [
                {
                "text": "deductible",
                "canonical_term": "Deductible"
                },
                {
                "text": "out of pocket maximum",
                "canonical_term": "Out-of-Pocket Loss/Limit/Maximum"
                }
            ],
            "EB02": [
                {
                "text": "myself",
                "cluster": "1"
                },
                {
                "text": "my family",
                "cluster": "2"
                }
            ],
            "EB06": [
                {
                "text": "this year",
                "cluster": "2"
                }
            ]
        },
        "unmapped_medical_terms": []
    }
    

    # 1. Initial extraction
    output = {
        "eb_filters": extract_eb_filters(response),
        "extracted_terms": extract_terms(response)
    }

    # 2. Terms for retrieval (EB03-only for now)
    retrieval_terms = extract_eb03_and_unmapped_terms(response)

    # 3. Call retrieval API (ONLY if terms exist)
    if retrieval_terms:
        api_response = retrieve_categories(retrieval_terms)

        print("\nAPI Response:")
        print(json.dumps(api_response, indent=2))

        # 4. Update EB filters using API output
        output["eb_filters"] = add_eb03_categories_from_api(
            output["eb_filters"],
            api_response
        )
    else:
        api_response = []


    # 5. Sort EB filters
    output["eb_filters"] = sort_eb_filters(output["eb_filters"])

    # 5.1 Ensure EB03 fallback
    output["eb_filters"] = ensure_default_eb03(output["eb_filters"])

    # 6. Final output
    final_output = {
        "Atomic_Questions": [
            {
                "eb_filters": output["eb_filters"],
                "extracted_terms": output["extracted_terms"]
            }
        ]
    }
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
