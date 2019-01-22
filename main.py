import csv

with open('mygpa.csv') as csv_file:
  csv_reader = csv.DictReader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      # print(f'Column names are {", ".join(row):10}')
      for i in row:
        # print()
        if i not in ("GPA", "r_weight", "cum_r_weight", "g_weight", "cum_g_weight", "score", "cum_score", "GPAX"):
          print("{:>13}  ".format(i), end="")
      print()
      # print(row)
      line_count += 1
    else:
      print(f'{row["user_id"]:>13.13}  {row["course_id"]:>13.13}  {row["course_name"]:>13.13}  {row["weight"]:>13.13}  {row["year"]:>13.13}  {row["term"]:>13.13}  {row["section"]:>13.13}  {row["grade"]:>13.13}')
      line_count += 1
  print(f'Processed {line_count} lines.')
