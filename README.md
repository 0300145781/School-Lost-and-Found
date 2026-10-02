[readme_md.md](https://github.com/user-attachments/files/32949850/readme_md.md)

# School Lost and Found Management System 

A robust, console-based Python application integrated with MySQL for managing lost and found items in a school environment. This system supports full database operations, matching algorithms, transaction logging, stack-based undo functionality, and robust error handling.

---

## Features & Menu Options

The application runs in an interactive loop presenting a 12-option menu:

1. **`add_student()`**: Inserts a new student record into the database.
2. **`report_lost()`**: Registers a lost item, pushes the transaction to an in-memory stack, and logs activity to `activity.txt`.
3. **`report_found()`**: Registers a found item, pushes the transaction to the stack, and logs activity to `activity.txt`.
4. **`view_items()`**: Displays all records from either the lost or found items table.
5. **`search_items()`**: Performs partial matches using SQL `LIKE` queries based on item name or category.
6. **`match_items()`**: Joins `lost_items` and `found_items` tables where names and categories match, and statuses are `'Open'` / `'Unclaimed'`.
7. **`claim_item()`**: Updates the status of both a lost item (`'Closed'`) and a found item (`'Returned'`).
8. **`delete_resolved()`**: Cleans up closed or returned records from the database.
9. **`reports()`**: Generates administrative summaries using SQL `GROUP BY`, `HAVING`, and `DISTINCT`.
10. **`undo_last()`**: Pops the last recorded transaction from the stack and rolls back/deletes that specific database entry (handles stack underflow gracefully).
11. **`display_stack()`**: Shows recent entries currently sitting in the stack memory.
12. **Exit**: Closes the database cursor and connection safely.

---

## Technical Stack & Architecture

* **Language**: Python
* **Database**: MySQL (`mysql.connector`)
* **Data Structures**: Stack (implemented using Python lists `[]`) for tracking actions and enabling undo features.
* **Error Handling**: Every database interaction is wrapped in `try/except` blocks to prevent crashes due to incorrect user inputs or SQL errors.
* **Logging**: Secondary logging performed via text files (`activity.txt`).

---

## Detailed Key Function Flowcharts

### 1. `report_lost()` (Option 2)
* Generates a unique ID (`lid = new_id(...)`).
* Prompts user for item details (item name, category, description, date, location, student ID).
* Executes a dynamic SQL insert query using string formatting.
* Upon success: Commits transaction, pushes `[table, id]` to the stack, writes to `activity.txt`, and prints success notification.
* Upon failure: Catches formatting or student ID errors and prompts the user.

### 2. `match_items()` (Option 6)
* Performs a SQL `JOIN` query between `lost_items` ($L$) and `found_items` ($F$).
* Filters criteria: matching `item_name` and `category`, where $L.\text{status} = \text{'Open'}$ and $F.\text{status} = \text{'Unclaimed'}$.
* Fetches all records (`mycursor.fetchall()`) and displays matching pairs (Lost ID, Item Name, Found ID, Location) or notifies the user if none exist.

### 3. `claim_item()` (Option 7)
* Accepts a lost item ID and found item ID from the user.
* Updates `lost_items` setting status to `'Closed'` where ID matches.
* Updates `found_items` setting status to `'Returned'` where ID matches.
* Commits changes, logs activity, and handles update exceptions.

### 4. `undo_last()` (Option 10)
* Pops the last action from the stack (`item = pop()`).
* Checks for stack underflow (`Stack empty?`).
* If entries exist, deletes the corresponding record from the database table using the popped ID, commits changes, and logs the removal to `activity.txt`.

---
