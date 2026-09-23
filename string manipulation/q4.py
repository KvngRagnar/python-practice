def summarise_amounts(raw_values):
    total = 0
    for raw in raw_values:
        try:
            total += int(raw)
        except:
            pass
    return {"total": total, "rejected": 0}

// Required example: ["10", " 5 ", "bad", "-3", "0", ""] must return {"total": 15, "rejected": 3}.
// Inputs are always strings; no other type validation is required.