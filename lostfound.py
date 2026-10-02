# School Lost and Found Management System

import mysql.connector as conn

# Database connection
mydb = conn.connect(host="localhost",
                    user="root",
                    password="nandu@2008",      
                    database="lostfound")
mycursor = mydb.cursor()

stack = []


# Text file
def write_log(msg):
    with open("activity.txt", "a") as F:
        F.write(msg + "\n")


# Generates next id
def new_id(table, col, prefix):
    mycursor.execute("select {} from {}".format(col, table))
    rows = mycursor.fetchall()
    n = 0
    for rec in rows:
        num = int(rec[0][1:])
        if num > n:
            n = num
    return prefix + str(n + 1).zfill(5)


# Stack 
def push(item):
    stack.append(item)


def pop():
    if len(stack) == 0:
        print("No entry left")
        return None
    else:
        return stack.pop()


def display_stack():
    if stack == []:
        print("Empty stack")
    else:
        print("Recent entries (latest first):")
        for k in stack[::-1]:
            print(k)


# Register student 
def add_student():
    try:
        sid = input("Enter student id (eg S00005): ")
        sname = input("Enter name: ")
        cls = input("Enter class (eg XII-A): ")
        phone = input("Enter phone no: ")
        q = "insert into students values('{}','{}','{}','{}')".format(sid, sname, cls, phone)
        mycursor.execute(q)
        mydb.commit()
        print("Student registered")
        write_log("Student " + sid + " registered")
    except:
        print("Error: student id may already exist")


#. Report  lost item 
def report_lost():
    try:
        lid = new_id("lost_items", "lid", "L")
        item = input("Enter item name: ")
        cat = input("Enter category (Bottle/Stationery/Card/Electronics/Other): ")
        desc = input("Enter description: ")
        d = input("Enter date lost (YYYY-MM-DD): ")
        loc = input("Enter location: ")
        sid = input("Enter student id of owner: ")
        q = "insert into lost_items values('{}','{}','{}','{}','{}','{}','{}','Open')".format(
            lid, item, cat, desc, d, loc, sid)
        mycursor.execute(q)
        mydb.commit()
        push(["lost_items", "lid", lid])
        print("Lost item reported, ID =", lid)
        write_log("Lost item " + lid + " reported")
    except:
        print("Error: check student id and date format")


# Report a found item
def report_found():
    try:
        fid = new_id("found_items", "fid", "F")
        item = input("Enter item name: ")
        cat = input("Enter category (Bottle/Stationery/Card/Electronics/Other): ")
        desc = input("Enter description: ")
        d = input("Enter date found (YYYY-MM-DD): ")
        loc = input("Enter location: ")
        sid = input("Enter student id of finder: ")
        q = "insert into found_items values('{}','{}','{}','{}','{}','{}','{}','Unclaimed')".format(
            fid, item, cat, desc, d, loc, sid)
        mycursor.execute(q)
        mydb.commit()
        push(["found_items", "fid", fid])
        print("Found item reported, ID =", fid)
        write_log("Found item " + fid + " reported")
    except:
        print("Error: check student id and date format")


# View all items
def view_items():
    ch = input("View (L for)Lost or (F for)Found items? ").upper()
    if ch == "L":
        mycursor.execute("select * from lost_items")
    elif ch == "F":
        mycursor.execute("select * from found_items")
    else:
        print("Invalid choice")
        return
    records = mycursor.fetchall()
    if len(records) == 0:
        print("No records")
    else:
        for rec in records:
            print(rec)
        print("Total records:", mycursor.rowcount)


# Search items
def search_items():
    word = input("Enter item name or category to search: ")
    print("--- Lost items ---")
    mycursor.execute("select * from lost_items where item_name like '%{}%' or category like '%{}%' order by lost_date".format(word, word))
    for rec in mycursor.fetchall():
        print(rec)
    print("--- Found items ---")
    mycursor.execute("select * from found_items where item_name like '%{}%' or category like '%{}%' order by found_date".format(word, word))
    for rec in mycursor.fetchall():
        print(rec)


# Match lost and found items
def match_items():
    q = ("select L.lid, L.item_name, L.location, F.fid, F.location "
         "from lost_items L, found_items F "
         "where L.item_name = F.item_name and L.category = F.category "
         "and L.status = 'Open' and F.status = 'Unclaimed'")
    mycursor.execute(q)
    records = mycursor.fetchall()
    if len(records) == 0:
        print("No matching items found")
    else:
        print("(Lost ID, Item, Lost at, Found ID, Found at)")
        for rec in records:
            print(rec)


# Mark item as returned
def claim_item():
    try:
        lid = input("Enter lost item id: ")
        fid = input("Enter found item id: ")
        mycursor.execute("update lost_items set status = 'Closed' where lid = '{}'".format(lid))
        mycursor.execute("update found_items set status = 'Returned' where fid = '{}'".format(fid))
        mydb.commit()
        print("Item marked as returned to owner")
        write_log("Item " + fid + " returned for " + lid)
    except:
        print("Error while updating")


# Delete resolved records 
def delete_resolved():
    ch = input("Delete all resolved records? (Y/N): ").upper()
    if ch == "Y":
        mycursor.execute("delete from lost_items where status = 'Closed'")
        mycursor.execute("delete from found_items where status = 'Returned'")
        mydb.commit()
        print("Resolved records deleted")
        write_log("Resolved records deleted")


# Reports
def reports():
    print("1. Lost items per category")
    print("2. Locations with 2 or more lost items")
    print("3. Distinct categories of found items")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        mycursor.execute("select category, count(*) from lost_items group by category")
    elif ch == 2:
        mycursor.execute("select location, count(*) from lost_items group by location having count(*) >= 2")
    elif ch == 3:
        mycursor.execute("select distinct category from found_items")
    else:
        print("Invalid choice")
        return
    for rec in mycursor.fetchall():
        print(rec)


# Undo last entry
def undo_last():
    item = pop()
    if item != None:
        q = "delete from {} where {} = '{}'".format(item[0], item[1], item[2])
        mycursor.execute(q)
        mydb.commit()
        print("Removed entry", item[2])
        write_log("Undo " + item[2])


# Main menu
while True:
    print()
    print("===== SCHOOL LOST AND FOUND SYSTEM =====")
    print("1. Register student")
    print("2. Report lost item")
    print("3. Report found item")
    print("4. View items")
    print("5. Search items")
    print("6. Match lost and found items")
    print("7. Mark item as returned")
    print("8. Delete resolved records")
    print("9. Reports")
    print("10. Undo last entry")
    print("11. Show recent entries")
    print("12. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number")
        continue

    if choice == 1:
        add_student()
    elif choice == 2:
        report_lost()
    elif choice == 3:
        report_found()
    elif choice == 4:
        view_items()
    elif choice == 5:
        search_items()
    elif choice == 6:
        match_items()
    elif choice == 7:
        claim_item()
    elif choice == 8:
        delete_resolved()
    elif choice == 9:
        reports()
    elif choice == 10:
        undo_last()
    elif choice == 11:
        display_stack()
    elif choice == 12:
        mycursor.close()
        mydb.close()
        print("Thank you")
        break
    else:
        print("Invalid choice")
