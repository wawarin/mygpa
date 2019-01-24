import csv
import re


class MyGPA:
  
    def __init__(self):
        self.running = True
        self.kw = ("SELECT", "FROM", "WHERE", "LIMIT")

    def commandSplit(self, cmd):
        cmd = re.split(" |,|'|\"|=", cmd)

        while "" in cmd:
            cmd.remove("")
        
        return cmd
    
    def openFile(self, file, cols, delimiter=","):
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
    
    def commandMode(self, cmd):
        if cmd[0].upper() in self.kw:
            if cmd[0].upper() == "SELECT":
                self.select(cmd[1:])
            elif cmd[0].upper() == "INSERT":
                print()
            elif cmd[0].upper() == "UPDATE":
                print()
        return 
    
    def select(self, cmd):
        newcmd = []
        for i in cmd:
            if i.upper() in self.kw:
                newcmd.append(i.upper())
            else:
                newcmd.append(i)
        cols = cmd[:newcmd.index("FROM")]
        table = cmd[newcmd.index("FROM") + 1]
        self.openFile(table, cols)
    
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
