import csv

with open('mygpa.csv') as csv_file:
  csv_reader = csv.DictReader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      print(f'Column names are {", ".join(row)}')
      line_count += 1
    else:
      print(f'\t{row["user_id"]} studies in the {row["course_name"]} course, and got {row["grade"]}.')
      line_count += 1
  print(f'Processed {line_count} lines.')
