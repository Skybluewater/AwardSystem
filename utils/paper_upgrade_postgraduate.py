from xlrd import open_workbook
import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account.models import User
from apps.account_profile.models import PaperRecord

paper_table = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(0)

stateChoice = {
    "第一层次": "f",
    "第二层次": "s",
    "第三层次": "t",
    "其他": "o"
}

for row in range(1, paper_table.nrows):
    line = paper_table.row_values(row)
    user = User.objects.get(student_id=line[0], isPostgraduate=True)
    title = line[10]
    if line[14] == "":
        state = "o"
    else:
        state = stateChoice[line[14]]
    PaperRecord.objects.filter(User=user, name=title, magzineName=line[11]).update(paperState=state)
    print(row)
