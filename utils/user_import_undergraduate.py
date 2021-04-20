from xlrd import open_workbook
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User

s = set()

grade_info_excel = open_workbook("../excels/grade_undergraduate.xlsx")
grade_info_table = grade_info_excel.sheet_by_index(0)
print("import excel successfully")

for row in range(1, grade_info_table.nrows):
    line = grade_info_table.row_values(row)
    studentID = line[0]
    if studentID in s:
        continue
    s.add(studentID)
    user = User.objects.create(student_id=studentID, username=studentID, password=make_password(studentID), email="%s@qq.com"%studentID)
    print(len(s), row)
