from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account.models import User
from apps.account_profile.models import CompetitionRecord
from apps.grade_info.models import SchoolYearInfo

competitionTable = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(5)

awardRange = {
    "特等": "u",
    "一等": "f",
    "金奖": "f",
    "二等": "s",
    "银奖": "s",
    "三等": "t",
    "铜奖": "t",
    "四等": "r",
    "其他": "o",
    "第三名": "t"
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
    CompetitionRecord.objects.filter(User=user, name=name, holder=holder, awardName=awardName, type="ra",
                                     certificateID=certificateNO, certificateDistributeOrganizationName=certificateOrg)\
        .update(awardLevel=awardValue, otherAward=otherAward)
    print(row)
