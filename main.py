import csv
import re


class MyGPA:
  
    def __init__(self):
        self.running = True
        self.kw = ("SELECT", "FROM", "WHERE", "LIMIT", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE")
        self.header = []

    def commandSplit(self, cmd):
        cmd = re.split(" |\(|\)|,|'|\"|=", cmd)

        while "" in cmd:
            cmd.remove("")
        
        while None in cmd:
            cmd.remove(None)
        
        return cmd
    
    def readFile(self, file, cols, conds=None, delimiter=","):
        try:
            with open(file + ".csv") as table:
                table_reader = csv.DictReader(table, delimiter=",")
                # tr = csv.reader(table, delimiter=",")
                # cells = list(tr)
                line_count = 0
                for row in table_reader:
                    if line_count == 0:
                        for c in row:
                            if cols != ["*"]:
                                if c in cols:
                                    print("{:>13}  ".format(c), end="")
                            else:
                                print("{:>13}  ".format(c), end="")
                        print()
                        if cols != ["*"]:
                            if conds is not None:
                                if row[conds[0]] == conds[1]:
                                    for i in cols:
                                        print("{:>13.13}  ".format(row[i]), end="")
                                    print()
                            else:
                                for i in cols:
                                    print("{:>13.13}  ".format(row[i]), end="")
                                print()
                        else:
                            if conds is not None:
                                if row[conds[0]] == conds[1]:
                                    for i in row:
                                        print("{:>13.13}  ".format(row[i]), end="")
                                    print()
                            else:
                                for i in row:
                                    print("{:>13.13}  ".format(row[i]), end="")
                                print()
                        line_count += 1
                    else:
                        if cols != ["*"]:
                            if conds is not None:
                                if row[conds[0]] == conds[1]:
                                    for i in cols:
                                        print("{:>13.13}  ".format(row[i]), end="")
                                    print()
                            else:
                                for i in cols:
                                    print("{:>13.13}  ".format(row[i]), end="")
                                print()
                        else:
                            if conds is not None:
                                if row[conds[0]] == conds[1]:
                                    for i in row:
                                        print("{:>13.13}  ".format(row[i]), end="")
                                    print()
                            else:
                                for i in row:
                                    print("{:>13.13}  ".format(row[i]), end="")
                                print()
                        line_count += 1
                print()
                # print(cells)
        except FileNotFoundError:
            print("TableNotFoundError:", "No such table: " + file)
        except KeyError:
            print("Column name error")
    
    def appendFile(self, file, cols, vals):
        if not self.header:
            with open(file + ".csv", mode="r") as fo:
                for row in csv.DictReader(fo, delimiter=","):
                    for i in row:
                        self.header.append(i)
                    break
            # print(header)
        with open(file + ".csv", mode="a", newline='') as fw:
            writer = csv.DictWriter(fw, self.header)
            # writer.writeheader()
            data = {}
            index = 0
            for i in range(len(self.header)):
                try:
                    if cols[index] == self.header[i]:
                        data[cols[index]] = vals[index]
                        index += 1
                    else:
                        data[self.header[i]] = ""
                except IndexError:
                    data[self.header[i]] = ""

            # fw.newlines()
            writer.writerow(data)
            print('Successfully inserted')
    
    def writeFile(self, file, cols, conds, action='update'):
        if not self.header:
            with open(file + ".csv", mode="r") as fo:
                for row in csv.DictReader(fo, delimiter=","):
                    for i in row:
                        self.header.append(i)
                    break
        with open(file + ".csv", mode="r") as fr:
            t = csv.reader(fr, delimiter=",")
            r = list(t)

        try:
            col = r[0].index(conds[0])
            try:
                row_arr = [r[i][col] for i in range(1, len(r))]
                row = row_arr.index(conds[1]) + 1
                try:
                    if cols is not None:
                        for i in range(0, len(cols), 2):
                            r[row][r[0].index(cols[i])] = cols[i + 1]
                    if action == "delete":
                        while True:
                            try:
                                num = row_arr.index(conds[1])
                                r.pop(num + 1)
                                row_arr.pop(num)
                            except ValueError:
                                break
                    with open(file + ".csv", mode="w", newline="") as fw:
                        writer = csv.writer(fw)
                        writer.writerows(r)
                    if action == 'update':
                        print("Update table successfully.")
                    elif action == 'delete':
                        print("Delete values successfully.")
                except ValueError:
                    print("ColumnError: Column '{}' does not exist.".format(cols[i]))
            except ValueError:
                print("ConditionError: Value '{}' does not exist.".format(conds[1]))
        except ValueError:
            print("ConditionError: Column '{}' does not exist.".format(conds[0]))
    
    # def deleteRow(self, file, cols, conds):
    #     pass

    def commandMode(self, cmd):
        if cmd[0].upper() in self.kw:
            if cmd[0].upper() == "SELECT":
                self.select(cmd[1:])
            elif cmd[0].upper() == "INSERT":
                self.insertVal(cmd[1:])
            elif cmd[0].upper() == "UPDATE":
                self.updateVal(cmd[1:])
            elif cmd[0].upper() == "DELETE":
                self.deleteRow(cmd[2:])
    
    def select(self, cmd):
        cmd = self.upperKW(cmd)
        cols = cmd[:cmd.index("FROM")]
        table = cmd[cmd.index("FROM") + 1]
        conds = None
        if 'WHERE' in cmd:
            conds = cmd[cmd.index("WHERE") + 1:]
        self.readFile(table, cols, conds=conds)
    
    def insertVal(self, cmd):
        cmd = self.upperKW(cmd)
        cols = cmd[2:cmd.index("VALUES")]
        vals = cmd[cmd.index("VALUES") + 1:]
        table = cmd[1]
        self.appendFile(table, cols, vals)
        # print(cmd)
    
    def updateVal(self, cmd):
        cmd = self.upperKW(cmd)
        cols = cmd[cmd.index("SET") + 1:cmd.index("WHERE")]
        conds = cmd[cmd.index("WHERE") + 1:]
        table = cmd[0]
        # print(cols, conds, table)
        self.writeFile(table, cols, conds)
    
    def deleteRow(self, cmd):
        cmd = self.upperKW(cmd)
        # cols = cmd[cmd.index("SET") + 1:cmd.index("WHERE")]
        conds = cmd[cmd.index("WHERE") + 1:]
        table = cmd[0]
        # print(cols, conds, table)
        self.writeFile(table, None, conds, 'delete')
    
    def upperKW(self, cmd):
        res = []
        for i in cmd:
            if i.upper() in self.kw:
                res.append(i.upper())
            else:
                res.append(i)
        return res
    
    def main(self):
        while self.running:
            incmd = input(">> ")

            cmd = self.commandSplit(incmd)
            # print(cmd)

            if len(cmd) == 1:
                if cmd[0].upper() == "EXIT":
                    self.running = False
                elif cmd[0].upper() in ("SELECT", "INSERT", "UPDATE"):
                    print("Incomplete command")
                else:
                    print("Error:", cmd[0] + ":", "command not found")
            elif len(cmd) > 1:
                # print(self.commandMode(cmd))
                self.commandMode(cmd)
        
        print("Program was terminated")


if __name__ == "__main__":
    app = MyGPA()
    app.main()

    # r = [[ 'a',  'b',  'c',  'd'],
    #      ['a1', 'b1', 'c1', 'd1'],
    #      ['a2', 'b2', 'c2', 'd2'],
    #      ['a3', 'b3', 'c3', 'd3']]
    
    # col = r[0].index('d')
    # row = [r[i][col] for i in range(1, len(r))].index('d2') + 1

    # r[row][r[0].index('b')] = 'b22'

    # print(r)

    # import operator

    # logic = {
    #     "AND": operator.and_,
    #     "OR": operator.or_,
    #     "NOT": operator.is_not
    # }

    # id = 2 AND user != 5 OR NOT (a = 2 AND b = 5)

    # print(logic['NOT'](1, 1))



# with open('mygpa.csv') as csv_file:
#   csv_reader = csv.DictReader(csv_file, delimiter=',')
#   line_count = 0
#   for row in csv_reader:
#     if line_count == 0:
#       # print(f'Column names are {", ".join(row):10}')
#       for i in row:
#         # print()
#         if i not in ("GPA", "r_weight", "cum_r_weight", "g_weight", "cum_g_weight", "score", "cum_score", "GPAX"):
#           print("{:>13}  ".format(i), end="")
#       print()
#       # print(row)
#       line_count += 1
#     else:
#       print(f'{row["user_id"]:>13.13}  {row["course_id"]:>13.13}  {row["course_name"]:>13.13}  {row["weight"]:>13.13}  {row["year"]:>13.13}  {row["term"]:>13.13}  {row["section"]:>13.13}  {row["grade"]:>13.13}')
#       line_count += 1
#   print(f'Processed {line_count} lines.')
