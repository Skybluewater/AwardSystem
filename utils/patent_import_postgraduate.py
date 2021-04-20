from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account.models import User
from apps.grade_info.models import SchoolYearInfo
from apps.account_profile.models import PatentRecord

patent_table = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(2)

for row in range(1, patent_table.nrows):
    line = patent_table.row_values(row)
    userID = User.objects.get(student_id=line[0], isPostgraduate=True)
    name = line[10]
    applyNumber = line[12]
    if "发明" in line[11]:
        applyClassify = "ip"
    else:
        applyClassify = "ot"
    applyTime = line[13]
    SchoolYearID = SchoolYearInfo.objects.get(schoolYearStart__lte=applyTime, schoolYearEnd__gt=applyTime)
    certificateNumber = line[14]
    approveDate = None
    if line[15]:
        approveDate = line[15]
    holdUnit = line[16]
    PatentRecord.objects.create(User=userID, SchoolYear=SchoolYearID, name=name, classify=applyClassify,
                                applyNumber=applyNumber, certificateNumber=certificateNumber, approveDate=approveDate,
                                holdUnit=holdUnit, applyTime=applyTime)
    print(row)


