# Trace and repair a function

## Easy  |  6 minutes  |  10 marks
    
    A ticket should cost 7 units. The developer expects three tickets to produce the integer 21.


def ticket_total(price, quantity):
    total = price * quantity
    print(total)
amount = ticket_total("7", 3)
print(amount)


Q1 Part B

    Explain why multiplication behaves this way and why amount does not contain the printed result. [3 marks]


Q1 Part A

    Before running the code, write the exact two output lines and state the value and type of amount. [4 marks]


Q1 Part C

    Rewrite the function and its call so the function returns an integer total and does not print internally. Print the returned result once outside the function. You may assume numeric integer inputs in the corrected version. [3 marks]

*find out why amount prints internally



# Find the missing passes

## Easy to moderate  |  9 minutes  |  15 marks


    Return every score greater than or equal to 50, in the original order. Inputs are lists of integers from 0 to 100. An empty list must return an empty list.


def passing_scores(scores):
    passed = []
    for index in range(len(scores) - 1):
        if scores[index] > 50:
            passed.append(scores[index])
    return passed
print(passing_scores([49, 50, 80, 65]))


Q2 Part B

    Correct the function without changing the input list. [6 marks]


Q2 Part C

    Write three executable assertions: one for the pass boundary 50, one for a single passing score, and one for an empty list. [4 marks]


Q2 Part A

    Predict the current printed output. Identify both independent defects and explain which result each defect loses. [5 marks]

# Protect the Original file
## Moderate  |  11 minutes  |  20 marks
    
    The function should return a new profile with an extra tag. The original profile and its tags must stay unchanged. The profile has only a string name and a list of string tags; both keys always exist.


def add_tag(profile, tag):
    updated = profile.copy()
    updated["tags"].append(tag)
    return updated
original = {"name": "Ada", "tags": ["python"]}
changed = add_tag(original, "testing")
print(original["tags"])
print(changed is original)
print(changed["tags"] is original["tags"])


Q3 Part A

    Before running the code, predict all three output lines. Explain what copy() copies here and which object is still shared. [7 marks]


Q3 Part C

    Write assertions showing that the original tags remain unchanged and the returned tags contain the new tag. Then append another tag to the returned list and assert that the original still has only its initial tag. [6 marks]


Q3 Part B

    Repair add_tag so its returned dictionary and tags list are independent of the original. Do not change the public function signature. [7 marks]


# Validate an import
## Challenging  |  13 minutes  |  25 marks
    
    You receive a list of strings representing whole-unit amounts. Return a dictionary with total and rejected. Use Python int(raw) conversion: surrounding whitespace is accepted. A converted amount of zero or more is valid. Negative amounts and strings that cannot be converted must each increase rejected by one. An empty list returns both values as zero. Do not change the input.


def summarise_amounts(raw_values):
    total = 0
    for raw in raw_values:
        try:
            total += int(raw)
        except:
            pass
    return {"total": total, "rejected": 0}


Required example: ["10", " 5 ", "bad", "-3", "0", ""] must return {"total": 15, "rejected": 3}. Inputs are always strings; no other type validation is required.


Q4 Part C

    Write four executable assertions covering the required mixed example, empty input, all rejected input, and a valid zero. State why checking only total could miss a bug. [8 marks]


Q4 Part B

    Rewrite the function to meet every rule. Catch only the expected conversion exception. [11 marks]


Q4 Part A

    Identify three defects or risks in the supplied function. Explain why a bare except can hide an unrelated failure. [6 marks]



# Make stock reservation reliable 
## Hardest  |  16 minutes  |  30 marks
    
    stock maps item names to available quantities. order is a list of (item, quantity) pairs. Stock values are non-negative integers; order quantities are integers, not booleans. Keys are strings. These shapes and types are guaranteed.

def reserve_stock(stock, order):
    remaining = stock.copy()
    for item, quantity in order:
        if quantity > stock[item]:
            raise ValueError("Insufficient stock")
        remaining[item] = stock[item] - quantity
    return remaining


Required behaviour
Return a new dictionary containing every stock key with its remaining quantity. Never modify stock or order, including when a request fails.

An item may occur more than once in order. Its combined requested quantity must be reserved. Never allow a negative remaining quantity.


Raise ValueError for an unknown item, a quantity of zero or less, or insufficient stock. Error message wording is your choice. An empty order returns an equal but separate dictionary.
You may use try/except with an assertion that fails if ValueError is not raised. Tests must call the function and check a result or failure, not just print it.


Q5 Part C

    Write four tests: successful repeated items, repeated items exceeding stock, an unknown item, and zero quantity. In the overselling test, make at least one earlier line valid, then assert the original stock is unchanged after the exception. Explain why editing a local copy protects the caller when a later line fails. [10 marks]


Q5 Part A

    With stock = {"pen": 5}, trace order = [("pen", 3), ("pen", 3)]. Explain why the supplied code incorrectly succeeds, and identify the other validation gaps. [6 marks]


Q5 Part B

    Repair the function to meet all requirements. Use only in-memory Python; no database or concurrency implementation is needed. [14 marks]
