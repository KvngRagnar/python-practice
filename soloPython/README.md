# Advanced Python Solo Assessment (4 Hours)

## Duration: 180 minutes. Build a command-line Campus Resource Management System in Python.

    Complete the required demonstration.


## Project scenario and functionality

    Learn2Earn lends equipment to fellows. Build a working Python program that stores resource inventory, issues items, accepts returns, searches inventory and produces accurate reports.

## REQUIREMENTS (70 marks):

1. Resource inventory (10): Every resource has unique ID, name, category, total units and available units. Add and list resources; reject duplicate IDs.

2. Borrowing (15): Check fellow ID and resource ID; quantity must be a positive integer and no greater than stock. Log every successful borrowing and reduce availability. Rejected attempts must not mutate state.

3. Returns (10): Only return quantities a fellow currently has on loan; update both borrowing records and inventory.

4. Search/filter (10): Case-insensitive name search; filter by category.

5. Reports (15): Show total units, available units, units currently borrowed, resources with fewer than 3 available units, and the resource with most units currently borrowed. If tied, identify all tied leaders.

6. Structure/robustness (10): Meaningful functions, menu that loops until exit, input validation and helpful errors.


No frameworks, databases, external services, or third-party packages required. Use Python standard library only. Your application should run locally.


## Starting data

resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []

## REQUIRED DEMONSTRATION, IN ORDER:

1. F001 borrows 2 laptops — available laptop units = 8.

2. F002 borrows 3 keyboards — available keyboard units = 2.

3. F001 returns 1 laptop — available laptop units = 9.

4. F003 requests 4 headsets — rejected without changing stock.

5. F002 tries to return 4 keyboards — rejected without changing stock.

6. Search for LAPtop — find Laptop, ignoring case.

7. Generate the report — overall units 18, available 14, borrowed 4, Keyboard low stock (2); Keyboard is most borrowed (3).

Optional bonus, maximum 5 bonus marks outside 100: persist and reload inventory and loans using JSON.

# Tasks

    A1. Source code or viewable source-code link 
        
        Manually graded. Paste your full Python code

    A2. Demonstration output and test evidence
        
        Manually graded. Paste actual run output for steps 1–7 and include one additional invalid-input test. Do not submit expected output as if you ran it.

    A3. Project design explanation
    
        Manually graded. Name at least four functions, explain how inventory and fellow loans are represented, and describe one design limitation.