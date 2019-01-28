import csv
import re


class MyGPA:
  
    def __init__(self):
        self.running = True
        self.kw = ("SELECT", "FROM", "WHERE", "LIMIT", "INSERT", "INTO", "VALUES")
        self.header = []

    def commandSplit(self, cmd):
        cmd = re.split(" |\(|\)|,|'|\"|=", cmd)

        while "" in cmd:
            cmd.remove("")
        
        while None in cmd:
            cmd.remove(None)
        
        return cmd
    
    def readFile(self, file, cols, delimiter=","):
        try:
            with open(file + ".csv") as table:
                table_reader = csv.DictReader(table, delimiter=",")
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
                        line_count += 1
                    else:
                        if cols != ["*"]:
                            for i in cols:
                                print("{:>13.13}  ".format(row[i]), end="")
                        else:
                            for i in row:
                                print("{:>13.13}  ".format(row[i]), end="")
                        print()
                        line_count += 1
                print()
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
        with open(file + ".csv", mode="a") as fw:
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
    
    def writeFile(self, file, cols, cons):
        if not self.header:
            with open(file + ".csv", mode="r") as fo:
                for row in csv.DictReader(fo, delimiter=","):
                    for i in row:
                        self.header.append(i)
                    break
        
        with open(file + ".csv", mode="w") as fw:
            pass
    
    def commandMode(self, cmd):
        if cmd[0].upper() in self.kw:
            if cmd[0].upper() == "SELECT":
                self.select(cmd[1:])
            elif cmd[0].upper() == "INSERT":
                self.insertVal(cmd[1:])
            elif cmd[0].upper() == "UPDATE":
                print()
    
    def select(self, cmd):
        newcmd = []
        for i in cmd:
            if i.upper() in self.kw:
                newcmd.append(i.upper())
            else:
                newcmd.append(i)
        cols = cmd[:newcmd.index("FROM")]
        table = cmd[newcmd.index("FROM") + 1]
        self.readFile(table, cols)
    
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
        cons = cmd[cmd.index("WHERE") + 1:]
        table = cmd[0]
        self.writeFile(table, cols, cons)
    
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
