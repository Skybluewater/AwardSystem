from xlrd import open_workbook
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.grade_info import LessonInfo, SchoolYearInfo, GradeInfo
from apps.account import User

grade_info_excel = open_workbook("../excels/grade_postgraduate.xlsx")
grade_info_table = grade_info_excel.sheet_by_index(0)
print("import excel successfully")

schoolList = SchoolYearInfo.objects.all()
lessonList = LessonInfo.objects.filter(lessonClass=1)

testFlag = {
    "重考": "re",
    "重修": "rs",
    "补考": "ee",
    "正常": "np",
    "旷考": "nt",
    "免修": "rl",
    "其它": "ot",
    "缓考": "tl"
}

optionFlag = {
    "必修": "mu",
    "选修": "ch",
    "专业必修课": "mu",
    "其他": "ot",
    "公共必修课": "mu",
    "专业选修课": "ch",
    "其它": "ot"
}

for row in range(1, grade_info_table.nrows):
    line = grade_info_table.row_values(row)
    try:
        userID = User.objects.get(student_id=line[0], isPostgraduate=True)
    except:
        print("**************************" + line[0])
    if line[1]:
        lessonID = line[1].replace("*", "")
        lessonID = lessonList.get(id=lessonID)
    else:
        lessonID = lessonList.get(lessonName=line[2], lessonClass=1)
    credit = line[7]
    if line[11]:
        grade = line[11].replace("请评教", "0")
    else:
        grade = 0
    schoolYear = line[8]
    if line[9] == "第一学期":
        schoolYear += "-1"
    else:
        schoolYear += "-2"
    schoolYearID = schoolList.get(schoolYearName=schoolYear)
    ifRestudied = False
    if line[14]:
        option = optionFlag[line[14]]
    else:
        option = "ot"
    if line[10]:
        testKind = testFlag[line[10]]
    else:
        testKind = testFlag["正常"]
    if testKind != "np" and testKind != "rl":
        ifRestudied = True
    GradeInfo.objects.create(SchoolYearID=schoolYearID, user=userID, LessonID=lessonID, credit=credit, grade=grade,
                             ifRestudied=ifRestudied, testKind=testKind)
    print(row)
