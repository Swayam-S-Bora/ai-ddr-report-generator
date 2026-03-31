def preprocess_text(inspection_text, thermal_text):
    # Simple rules to enhance reasoning

    enhanced_context = ""

    if "tile joint" in inspection_text.lower():
        enhanced_context += "\nPossible cause: water seepage through tile joints."

    if "crack" in inspection_text.lower():
        enhanced_context += "\nPossible cause: external structural cracks allowing water ingress."

    if "coldspot" in thermal_text.lower():
        enhanced_context += "\nThermal analysis indicates moisture presence."

    return enhanced_context