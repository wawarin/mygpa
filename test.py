import csv


while True:
    cmd = input(">> ")

    kw = ("SELECT", "FROM", "WHERE", "ORDER", "BY", "LIMIT", "INSERT", "INTO")

    cmd = cmd.split()

    def openCSV(dir, cols, delimeter=","):
        cols = (cols)
        with open(dir) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=delimeter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    for i in row:
                        # if cols == "*" or i in ("GPA", "r_weight", "cum_r_weight", "g_weight", "cum_g_weight", "score", "cum_score", "GPAX"):
                        if cols == "*" or i in cols:
                            print("{:>13}  ".format(i), end="")
                    print()
                    line_count += 1
                else:
                    # print(f'\t{row["user_id"]} studies in the {row["course_name"]} course, and got {row["grade"]}.')
                    line_count += 1
            print(f'Processed {line_count} lines.')

    def select(cmd):
        try:
            open(cmd[2] + ".csv")
            # if cmd[0] == "*":
                # view all cols
            openCSV(cmd[2] + ".csv", cmd[0])
            # elif cmd[0] in 
        except FileNotFoundError:
            print("TableNotFoundError:", "No such table: " + cmd[2])

        # if cmd[0] == "*":
        #     if cmd[1].upper() in kw:
        #         if cmd[1].upper() == "FROM":
        #             openCSV(cmd[2] + ".csv")
        # else:
        #     if cmd[0]:
        #         pass

    if cmd != []:
        if cmd[0].upper() in kw:
            if cmd[0].upper() == "SELECT":
                select(cmd[1:])
        else:
            if cmd[0].upper() == "EXIT":
                break


    # print(cmd[1:])
