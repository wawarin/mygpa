import re

usr = "select col1 as c1,col2 as 1,col3 as 1,col4 as 1 from table order by id limit 1"

usr = re.split(" |,", usr)

kw = ("SELECT", "FROM", "WHERE", "ORDER", "BY", "ASC", "DSC", "LIMIT")
cmd = {}
i = 0

while i < len(usr):
    if usr[i] == "":
        usr.pop(i)
    if usr[i].upper() in kw:
        cmd[usr[i].upper()] = i
    i += 1

cols = usr[cmd["SELECT"] + 1:cmd["FROM"]]

try:
    table = usr[cmd["FROM"] + 1: cmd["WHERE"]]
except KeyError:
    try:
        table = usr[cmd["FROM"] + 1: cmd["ORDER"]]
    except KeyError:
        try:
            table = usr[cmd["FROM"] + 1: cmd["LIMIT"]]
        except KeyError:
            table = usr[cmd["FROM"] + 1:]

try:
    conds = usr[cmd["WHERE"] + 1: cmd["ORDER"]]
except KeyError:
    try:
        conds = usr[cmd["WHERE"] + 1:]
    except KeyError:
        conds = []

try:
    limit = usr[cmd["LIMIT"] + 1:]
except KeyError:
    limit = []

print(cmd)
print(usr)
print(cols)
print(table)
print(conds)
print(limit)
