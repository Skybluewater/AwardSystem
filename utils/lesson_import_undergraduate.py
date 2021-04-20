from xlrd import open_workbook
import django
import re
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AwardSystem.settings")
django.setup()

from apps.grade_info import LessonInfo, MajorInfo, SchoolYearInfo

s = set()

grade_info_excel = open_workbook("../excels/grade_undergraduate.xlsx")
grade_info_table = grade_info_excel.sheet_by_index(0)
print("import excel successfully")

majorList = MajorInfo.objects.all()

dic = {
    "公共基础课程": "cb",
    "体育课": "pe",
    "大类基础": "lb",
    "专业课": "pf",
    "校公选课": "cc",
    "扩展英语": "ee",
    "实践环节": "ps",
    "基础教育": "eb",
    "平台基础": "fb",
    "社会证书": "sc",
    "专业基础课程": "pb",
}

LessonList = []

for row in range(1, grade_info_table.nrows):
    line = grade_info_table.row_values(row)
    lessonID = line[4]
    if lessonID in s:
        continue
    s.add(lessonID)
    lessonName = line[5]
    lessonAttribute = line[6]
    credit = line[11]
    schoolYear = re.match(r"^[(]20\d\d-20\d\d-\d[)]|20\d\d20\d\d\d", line[1]).group()
    if schoolYear[0] == "(":
        schoolYear = schoolYear.replace('(', '').replace(')', '')
    else:
        schoolYear = schoolYear[0:4] + '-' + schoolYear[4:8] + '-' + schoolYear[8]
    try:
        schoolYearID = SchoolYearInfo.objects.get(schoolYearName=schoolYear)
    except:
        print(row, schoolYear)
    AffiliatedMajor = majorList.get(SchoolYearID=schoolYearID, studentNum=240)
    classification = ""
    if line[6] in dic:
        classification = dic[line[6]]
    else:
        classification = "ot"
    lessonID = lessonID.replace("SPA", "")
    lesson = LessonInfo.objects.create(id=lessonID, lessonName=lessonName, classification=classification,
                        credit=credit, SchoolYearID=schoolYearID, lessonClass=0)
    lesson.AffiliatedMajor.add(AffiliatedMajor)
    print(len(s))
