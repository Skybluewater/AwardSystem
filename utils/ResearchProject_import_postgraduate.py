from xlrd import open_workbook
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User
from apps.grade_info import SchoolYearInfo
from apps.

account_profile.models import ResearchProject

research_table = open_workbook("../excels/award_postgraduate.xlsx").sheet_by_index(3)

projectChoices = {
    "国家自然科学基金面上项目": "ns",
    "国家自然科学基金其他项目": "no",
    "国家自然科学基金重点项目": "nm",
    "国家自然科学基金重大项目": "ng",
    "国防科技重点实验基金项目": "dm",
    "973项目": "p9",
    "863项目": "p8",
    "其他": "ot"
}

for row in range(1, research_table.nrows):
    line = research_table.row_values(row)
    user = User.objects.get(student_id=line[0], isPostgraduate=True)
    schoolYear = SchoolYearInfo.objects.get(schoolYearStart__lte=line[7], schoolYearEnd__gt=line[7])
    name = line[10]
    projectType = projectChoices[line[11]]
    projectWork = line[12]
    ResearchProject.objects.create(User=user, SchoolYearInfo=schoolYear, name=name, projectType=projectType, projectWork=projectWork)
    print(row)
