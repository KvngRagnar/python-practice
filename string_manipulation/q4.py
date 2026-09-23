def summarise_amounts(raw_values):
    total = 0
    rejected = 0
    for raw in raw_values:
        try:

            if int(raw) >= 0:
                total += int(raw)
            else:
                rejected += 1
        except ValueError:
            rejected += 1
    return {"total": total, "rejected": 0}
d = summarise_amounts(["10", " 5 ", "bad", "-3", "0", ""])
print(d)
#Required example:  must return {"total": 15, "rejected": 3}.
#Inputs are always strings; no other type validation is required.