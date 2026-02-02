def segment_layout(image_paths: list[str]) -> list[dict]:
    """
    Layout-aware segmentation with clause IDs.
    """
    blocks = []
    clause_counter = 1

    for img in image_paths:
        blocks.append({
            "clause_id": f"CL-{clause_counter}",
            "source_image": img,
            "text": "Simulated clause text from layout model",
            "type": "clause",
        })
        clause_counter += 1

    return blocks

