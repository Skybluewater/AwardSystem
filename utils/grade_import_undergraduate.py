from xlrd import open_workbook
import django
import re
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.account import User
from apps.grade_info import SchoolYearInfo, LessonInfo, GradeInfo

grade_table = open_workbook("../excels/grade_undergraduate.xlsx")
grade_sheet = grade_table.sheet_by_index(0)
print("excel read already")

testFlag = {
    "重考": "re",
    "重修": "rs",
    "补考": "ee",
    "正常考试": "np",
    "旷考": "nt",
    "免修": "rl"
}

optionFlag = {
    "必修": "mu",
    "选修": "ch",
    "任选": "ei",
}

gradeFlag = {
    "中等": 75,
    "合格": 60,
    "良好": 85,
    "通过": 60,
    "优秀": 95,
    "不合格": 55,
    "及格": 65,
    "免修": 85
}

for row in range(1, grade_sheet.nrows):
    line = grade_sheet.row_values(row)
    userID = User.objects.get(student_id=line[0])
    lessonID = line[4].replace("SPA", "")
    credit = line[11]
    grade = line[7]
    schoolYear = re.match("\(*20\d\d-*20\d\d-*\d", line[1]).group()
    if schoolYear[0] == "(":
        schoolYear = schoolYear.replace("(", "")
    else:
        schoolYear = schoolYear[0:4] + "-" + schoolYear[4:8] + "-" + schoolYear[8]
    schoolYearID = SchoolYearInfo.objects.get(schoolYearName=schoolYear)
    lesson = LessonInfo.objects.get(id=lessonID)
    if line[14] in optionFlag:
        option = optionFlag[line[14]]
    else:
        option = "ot"
    testKind = testFlag[line[16]]
    if grade in gradeFlag:
        grade = gradeFlag[grade]
    ifRestudied = False
    if testKind != "np" and testKind != "rl":
        ifRestudied = True
    GradeInfo.objects.create(SchoolYearID=schoolYearID, user=userID, LessonID=lesson, credit=credit,
                             grade=grade, ifRestudied=ifRestudied, testKind=testKind, optionChoice=option)
    print(row)
