from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.award_info.models import AwardInfo
from apps.grade_info.models import MajorInfo, SchoolYearInfo

award_table = open_workbook("../excels/award_postgraduate.xlsx")

SchoolYearList = SchoolYearInfo.objects.all()[:8]
s = set()

for i in range(0, award_table.nsheets):
    award_sheet = award_table.sheet_by_index(i)
    for row in range(1, award_sheet.nrows):
        line = award_sheet.row_values(row)
        name = line[1]
        if name == "" or name in s:
            continue
        s.add(name)
        for schoolYearID in SchoolYearList:
            award = AwardInfo.objects.create(name=name, SchoolYear=schoolYearID, ifHasClass=False, amount=0,
                                             addition="", money=0)
            Major = MajorInfo.objects.get(isPostgraduate=True, SchoolYearID=schoolYearID)
            award.Major.add(Major)
        print(len(s))
