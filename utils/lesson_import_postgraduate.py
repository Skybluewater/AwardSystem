from xlrd import open_workbook

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.grade_info import LessonInfo, MajorInfo, SchoolYearInfo

s = set()

grade_info_excel = open_workbook("../excels/grade_postgraduate.xlsx")
grade_info_table = grade_info_excel.sheet_by_index(0)
print("import excel successfully")

majorList = MajorInfo.objects.all()
schoolList = SchoolYearInfo.objects.all()
dic = {
    "未分类课": "uc",
    "公共必修课": "cm",
    "专业必修课": "pm",
    "选修课": "op",
    "专业课": "pf",
    "专业选修课": "po",
}

for row in range(1, grade_info_table.nrows):
    line = grade_info_table.row_values(row)
    lessonID = ""
    if line[1]:
        lessonID = line[1].replace("*", "")
    if line[1] and lessonID in s:
        continue
    elif not line[1] and line[2] in s:
        continue
    elif not line[1] and line[2] not in s:
        s.add(line[2])
    else:
        s.add(lessonID)
    lessonName = line[2]
    classification = dic[line[4]]
    credit = line[7]
    schoolYear = line[8]
    if line[9] == "第一学期":
        schoolYear += "-1"
    else:
        schoolYear += "-2"
    schoolYearID = schoolList.get(schoolYearName=schoolYear)
    try:
        AffiliatedMajor = majorList.get(SchoolYearID=schoolYearID, studentNum=100)
    except:
        print(schoolYear)
    if line[1]:
        lesson = LessonInfo.objects.create(id=lessonID, lessonName=lessonName, classification=classification,
                                           credit=credit, SchoolYearID=schoolYearID, lessonClass=1)
    else:
        lesson = LessonInfo.objects.create(lessonName=lessonName, classification=classification,
                                           credit=credit, SchoolYearID=schoolYearID, lessonClass=1)
    lesson.AffiliatedMajor.add(AffiliatedMajor)
    print(row, len(s))
