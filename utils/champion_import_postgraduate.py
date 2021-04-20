from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account.models import User
from apps.account_profile.models import CompetitionRecord
from apps.grade_info.models import SchoolYearInfo

competitionTable = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(5)

competitionRange = {
    "国家级": "na",
    "国际级": "in",
    "省部级": "ds",
    "学校级": "lr",
    "学院级": "cl",
    "其他": "ot"
}

awardRange = {
    "特等奖": "u",
    "一等奖": "f",
    "二等奖": "s",
    "三等奖": "t",
    "四等奖": "r",
    "其他": "o"
}

for row in range(1, competitionTable.nrows):
    line = competitionTable.row_values(row)
    user = User.objects.get(student_id=line[0], isPostgraduate=True)
    name = line[10]
    if line[11]:
        holder = line[11]
    else:
        holder = "其他"
    if line[12]:
        awardName = line[12]
    else:
        awardName = "其他"
    competeRange = competitionRange[line[13]]
    schoolYearID = SchoolYearInfo.objects.get(schoolYearStart__lte=line[14], schoolYearEnd__gt=line[14])
    awardValue = ""
    for key, value in awardRange.items():
        if key in line[15]:
            awardValue = awardRange[key]
    otherAward = ""
    if awardValue == "":
        otherAward = line[15]
        awardValue = 'o'
    certificateNO = line[18].replace("无", "")
    certificateOrg = line[19]
    CompetitionRecord.objects.create(User=user, SchoolYear=schoolYearID, name=name, holder=holder, awardName=awardName,
                                     competeRange=competeRange, awardLevel=awardValue, otherAward=otherAward,
                                     certificateID=certificateNO, certificateDistributeOrganizationName=certificateOrg)
    print(row)
