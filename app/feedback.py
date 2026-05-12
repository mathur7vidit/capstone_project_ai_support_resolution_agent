from app.safety import mask_pii


feedback_store = []


def save_feedback(query, response, rating):

    feedback_store.append({
        "query": mask_pii(query),
        "response": mask_pii(response),
        "rating": rating
    })


def should_reduce_response_length():

    low_ratings = [
        x for x in feedback_store
        if x["rating"] <= 2
    ]

    return len(low_ratings) >= 3
