import os
import django
from xlrd import open_workbook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from apps.award_info.models import AwardInfo
from apps.account_profile.models import User, AwardHistory
from apps.grade_info.models import SchoolYearInfo

user_table = open_workbook("../excels/award_postgraduate.xlsx")

k = 0

for book in range(0, user_table.nsheets):
    users = user_table.sheet_by_index(book)
    for row in range(1, users.nrows):
        line = users.row_values(row)
        if line[1] == "":
            continue
        userID = User.objects.get(student_id=line[0], isPostgraduate=True)
        schoolYear = SchoolYearInfo.objects.get(schoolYearStart__lte=line[7], schoolYearEnd__gt=line[7])
        name = line[1]
        awardInfo = AwardInfo.objects.get(SchoolYear=schoolYear, name=name)
        try:
            AwardHistory.objects.get(User=userID, AwardYear=schoolYear, AwardID=awardInfo)
        except ObjectDoesNotExist:
            history = AwardHistory.objects.create(AwardYear=schoolYear, AwardID=awardInfo, awardName=name)
            history.User.add(userID)
            k += 1
            print(k)
