"""GiscoHub Campus Resource Management System (standard library only).

Run interactive menu:  python giscohub.py
Run required demo:     python giscohub.py --demo
"""
import json
import os
import sys

DATA_FILE = "giscohub_data.json"
LOW_STOCK_THRESHOLD = 3

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
# Each record: {"fellow_id", "resource_id", "quantity", "returned"}
# Units still on loan for a record = quantity - returned.
borrow_records = []


# ---------------------------------------------------------------- helpers
def parse_positive_int(text):
    """Return int if text is a positive integer string, else None."""
    text = str(text).strip()
    if text.isdigit() and int(text) > 0:
        return int(text)
    return None


def find_resource(resource_id):
    rid = str(resource_id).strip().upper()
    for r in resources:
        if r["id"] == rid:
            return r
    return None


def outstanding(fellow_id, resource_id):
    """Units this fellow currently has on loan for this resource."""
    return sum(rec["quantity"] - rec["returned"] for rec in borrow_records
               if rec["fellow_id"] == fellow_id and rec["resource_id"] == resource_id)


# ---------------------------------------------------------------- inventory
def add_resource(rid, name, category, total):
    rid, name, category = str(rid).strip().upper(), str(name).strip(), str(category).strip()
    if not rid or not name or not category:
        return False, "ID, name and category cannot be empty."
    if find_resource(rid):
        return False, f"Duplicate ID: {rid} already exists."
    qty = parse_positive_int(total)
    if qty is None:
        return False, "Total units must be a positive integer."
    resources.append({"id": rid, "name": name, "category": category,
                      "total": qty, "available": qty})
    return True, f"Added {name} ({rid}) with {qty} units."


def format_resources(items):
    if not items:
        return "  (no resources found)"
    lines = [f"  {'ID':<6}{'Name':<14}{'Category':<14}{'Total':>6}{'Avail':>7}"]
    for r in items:
        lines.append(f"  {r['id']:<6}{r['name']:<14}{r['category']:<14}"
                     f"{r['total']:>6}{r['available']:>7}")
    return "\n".join(lines)


# ---------------------------------------------------------------- borrowing
def borrow(fellow_id, resource_id, quantity):
    """Validate everything first; mutate state only if all checks pass."""
    fellow_id = str(fellow_id).strip().upper()
    if fellow_id not in fellows:
        return False, f"Unknown fellow ID: {fellow_id}"
    res = find_resource(resource_id)
    if res is None:
        return False, f"Unknown resource ID: {str(resource_id).strip().upper()}"
    qty = parse_positive_int(quantity)
    if qty is None:
        return False, "Quantity must be a positive whole number."
    if qty > res["available"]:
        return False, (f"Rejected: only {res['available']} {res['name']} unit(s) "
                       f"available, {qty} requested.")
    res["available"] -= qty
    borrow_records.append({"fellow_id": fellow_id, "resource_id": res["id"],
                           "quantity": qty, "returned": 0})
    return True, (f"{fellows[fellow_id]} borrowed {qty} {res['name']}. "
                  f"Available now: {res['available']}")


# ---------------------------------------------------------------- returns
def return_item(fellow_id, resource_id, quantity):
    fellow_id = str(fellow_id).strip().upper()
    if fellow_id not in fellows:
        return False, f"Unknown fellow ID: {fellow_id}"
    res = find_resource(resource_id)
    if res is None:
        return False, f"Unknown resource ID: {str(resource_id).strip().upper()}"
    qty = parse_positive_int(quantity)
    if qty is None:
        return False, "Quantity must be a positive whole number."
    held = outstanding(fellow_id, res["id"])
    if qty > held:
        return False, (f"Rejected: {fellows[fellow_id]} has only {held} "
                       f"{res['name']} on loan, tried to return {qty}.")
    remaining = qty
    for rec in borrow_records:  # settle oldest loans first
        if remaining == 0:
            break
        if rec["fellow_id"] == fellow_id and rec["resource_id"] == res["id"]:
            take = min(remaining, rec["quantity"] - rec["returned"])
            rec["returned"] += take
            remaining -= take
    res["available"] += qty
    return True, (f"{fellows[fellow_id]} returned {qty} {res['name']}. "
                  f"Available now: {res['available']}")


# ---------------------------------------------------------------- search
def search_by_name(term):
    term = str(term).strip().lower()
    return [r for r in resources if term and term in r["name"].lower()]


def filter_by_category(category):
    category = str(category).strip().lower()
    return [r for r in resources if r["category"].lower() == category]


# ---------------------------------------------------------------- reports
def generate_report():
    total = sum(r["total"] for r in resources)
    available = sum(r["available"] for r in resources)
    per_resource = {r["id"]: sum(rec["quantity"] - rec["returned"]
                                 for rec in borrow_records
                                 if rec["resource_id"] == r["id"])
                    for r in resources}
    borrowed = sum(per_resource.values())
    low = [r for r in resources if r["available"] < LOW_STOCK_THRESHOLD]
    top = max(per_resource.values(), default=0)
    leaders = [r for r in resources if per_resource[r["id"]] == top] if top > 0 else []

    out = ["=== INVENTORY REPORT ===",
           f"Total units:               {total}",
           f"Available units:           {available}",
           f"Units currently borrowed:  {borrowed}",
           f"Resources with fewer than {LOW_STOCK_THRESHOLD} available:"]
    if low:
        out += [f"  - {r['name']} ({r['available']})" for r in low]
    else:
        out.append("  (none)")
    if leaders:
        label = "Most borrowed resource" if len(leaders) == 1 else "Most borrowed (TIE)"
        out.append(f"{label}:")
        out += [f"  - {r['name']} ({top})" for r in leaders]
    else:
        out.append("Most borrowed resource: none (nothing currently on loan)")
    return "\n".join(out)


# ---------------------------------------------------------------- persistence (bonus)
def save_data(path=DATA_FILE):
    with open(path, "w") as f:
        json.dump({"resources": resources, "fellows": fellows,
                   "borrow_records": borrow_records}, f, indent=2)


def load_data(path=DATA_FILE):
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        resources[:] = data["resources"]
        borrow_records[:] = data["borrow_records"]
        fellows.clear()
        fellows.update(data["fellows"])
        return True
    except (ValueError, KeyError, OSError):
        print("Warning: data file unreadable; using starting data.")
        return False


# ---------------------------------------------------------------- menu
MENU = """
===== GiscoHub Resource Manager =====
1. List resources      5. Search by name
2. Add resource        6. Filter by category
3. Borrow              7. Report
4. Return              0. Exit"""


def run_menu():
    if load_data():
        print(f"Loaded saved data from {DATA_FILE}.")
    while True:
        print(MENU)
        try:
            choice = input("Choose: ").strip()
        except EOFError:
            choice = "0"
        if choice == "1":
            print(format_resources(resources))
        elif choice == "2":
            ok, msg = add_resource(input("ID: "), input("Name: "),
                                   input("Category: "), input("Total units: "))
            print(msg)
        elif choice in ("3", "4"):
            fid, rid, q = input("Fellow ID: "), input("Resource ID: "), input("Quantity: ")
            ok, msg = (borrow if choice == "3" else return_item)(fid, rid, q)
            print(msg)
        elif choice == "5":
            print(format_resources(search_by_name(input("Name contains: "))))
        elif choice == "6":
            print(format_resources(filter_by_category(input("Category: "))))
        elif choice == "7":
            print(generate_report())
        elif choice == "0":
            save_data()
            print(f"Data saved to {DATA_FILE}. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from the menu (0-7).")
            continue
        if choice in ("2", "3", "4"):
            save_data()


# ---------------------------------------------------------------- demo
def stock(name):
    return next(r["available"] for r in resources if r["name"] == name)


def snapshot():
    return json.dumps([resources, borrow_records], sort_keys=True)


def run_demo():
    print("1. F001 borrows 2 laptops")
    print("  ", borrow("F001", "R001", 2), "-> laptop available =", stock("Laptop"))
    print("2. F002 borrows 3 keyboards")
    print("  ", borrow("F002", "R002", 3), "-> keyboard available =", stock("Keyboard"))
    print("3. F001 returns 1 laptop")
    print("  ", return_item("F001", "R001", 1), "-> laptop available =", stock("Laptop"))
    print("4. F003 requests 4 headsets (only 3 exist)")
    before = snapshot()
    print("  ", borrow("F003", "R003", 4))
    print("   state unchanged:", before == snapshot(), "| headset available =", stock("Headset"))
    print("5. F002 tries to return 4 keyboards (has 3)")
    before = snapshot()
    print("  ", return_item("F002", "R002", 4))
    print("   state unchanged:", before == snapshot(), "| keyboard available =", stock("Keyboard"))
    print("6. Search for 'LAPtop'")
    print(format_resources(search_by_name("LAPtop")))
    print("7. Report")
    print(generate_report())
    print("\nExtra invalid-input tests")
    before = snapshot()
    for label, result in [
        ("quantity 'abc'", borrow("F001", "R001", "abc")),
        ("quantity -2", borrow("F001", "R001", "-2")),
        ("quantity 0", borrow("F001", "R001", "0")),
        ("unknown fellow F999", borrow("F999", "R001", 1)),
        ("unknown resource R999", borrow("F001", "R999", 1)),
        ("duplicate resource ID R001", add_resource("R001", "Mouse", "Accessories", 4)),
    ]:
        print(f"   {label}: {result}")
    print("   state unchanged after all invalid inputs:", before == snapshot())


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()