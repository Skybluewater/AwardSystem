from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User
from apps.grade_info import SchoolYearInfo
from apps.account_profile import PublishRecord

publishRecord = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(1)

for row in range(1, publishRecord.nrows):
    line = publishRecord.row_values(row)
    user = User.objects.get(student_id=line[0], isPostgraduate=True)
    schoolYear = SchoolYearInfo.objects.get(schoolYearStart__lte=line[14], schoolYearEnd__gt=line[14])
    name = line[10]
    publish_house = line[11]
    work_contribute = line[12]
    book = line[13]
    publish_date = line[14]
    publish_type = line[15]
    author_amount = int(line[16])
    author_self = line[17]
    PublishRecord.objects.create(User=user, SchoolYear=schoolYear, name=name, publishing_house=publish_house, contribution=work_contribute, publish_date=publish_date, publishType=publish_type, authorAmount=author_amount, authorNum=author_self)
