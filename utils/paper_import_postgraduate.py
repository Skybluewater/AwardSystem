from xlrd import open_workbook
import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User
from apps.account_profile import PaperRecord
from apps.grade_info import SchoolYearInfo

paper_table = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(0)

postChoice = {
    "在线发表": "po",
    "正式发表": "pa",
    "其它": "ot"
}

conferenceChoice = {
    "国际会议": "ic",
    "重要期刊": "im",
    "顶级期刊": "tm",
    "其他SCI期刊": "os",
    "国际期刊": "om",
    "国内期刊": "nm",
    "国内会议": "nc",
    "其它": "ot"
}

orderChoice = {
    "第一作者": "f",
    "第二作者": "s",
    "第三作者": "t",
    "共同第一作者": "r",
    "其它": "o"
}

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
    conferenceOption = conferenceChoice[line[12]]
    if line[17]:
        totalReference = line[17]
    else:
        totalReference = 0
    if line[18]:
        publishStatus = postChoice[line[18]]
    else:
        publishStatus = "ot"
    if line[19]:
        line[19] = line[19].replace(" ", "").replace("月", ".").replace("年", ".").replace("日", ".").replace("/", ".").replace(".", "-")
        year_month = re.match(".*20\d\d-\d", line[19]).group().replace("-0", "-1")
        publishDate = year_month + "-15"
    else:
        publishDate = "2020-01-01"
    schoolYear = SchoolYearInfo.objects.get(schoolYearStart__lte=publishDate, schoolYearEnd__gt=publishDate)
    auth = ""
    if line[20]:
        if "本人第一作者" in line[20]:
            auth = "f"
        elif "本人第二作者" in line[20]:
            auth = "s"
        elif "共同第一作者" in line[20]:
            auth = "r"
        else:
            auth = "t"
    else:
        auth = "t"
    if line[14] == "":
        state = "o"
    else:
        state = stateChoice[line[14]]
    PaperRecord.objects.create(User=user, name=title, magzineName=line[11], authOrder=auth,
                               postStatus=publishStatus, totalReference=totalReference,
                               conferenceChoice=conferenceOption, publishDate=publishDate, SchoolYear=schoolYear, paperState=state)
    print(row)
