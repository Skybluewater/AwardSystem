from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User
from apps.account_profile import HonorTitle
from apps.grade_info import SchoolYearInfo

honor_table = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(7)

honorChoice = {
    "国际级": "in",
    "国家级": "na",
    "省部级": "ds",
    "其他": "ot",
    "学校级": "co",
    "学院级": "ac"
}

for row in range(1, honor_table.nrows):
    line = honor_table.row_values(row)
    user = User.objects.get(student_id=line[0], isPostgraduate=True)
    name = line[10]
    prize = honorChoice[line[11]]
    proclaimUnit = line[12]
    if line[13]:
        date = line[13]
    else:
        date = "2020-01-01"
    schoolYear = SchoolYearInfo.objects.get(schoolYearStart__lte=date, schoolYearEnd__gt=date)
    HonorTitle.objects.create(User=user, SchoolYear=schoolYear, honorName=name, proclaimOrganization=proclaimUnit, honorRank=prize, issueDate=date, type="ot")
    print(row)
