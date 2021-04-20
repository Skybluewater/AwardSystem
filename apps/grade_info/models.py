from django.db import models
from apps.account.models import User
from database.base_model import BaseModel


# Create your models here.
class DeptInfo(models.Model):  # 学院信息
    deptName = models.CharField(max_length=25, verbose_name="学院名称")
    deptAbstract = models.TextField(verbose_name="学院简介")


class SchoolYearInfo(models.Model):  # 学年信息
    # schoolYearPeriod = models.DurationField(verbose_name="学年时间段")
    schoolYearName = models.TextField(verbose_name="学年名称")
    schoolYearStart = models.DateField(default=9999 - 12 - 31, verbose_name="起始日期")
    schoolYearEnd = models.DateField(default=9999 - 12 - 31, verbose_name="终止日期")


# TODO
class GradeInfo(models.Model):  # 个人成绩信息
    reExam = "re"
    reStudied = "rs"
    extraExam = "ee"
    passed = "np"
    notPresent = "nt"
    regardless = "rl"
    testLater = "tl"

    testFlag = (
        (reExam, "重考"),
        (reStudied, "重修"),
        (passed, "正常考试"),
        (extraExam, "补考"),
        (notPresent, "旷考"),
        (regardless, "免修"),
        (testLater, "缓考"),
        ("ot", "其它"),

    )

    must = "mu"
    choice = "ch"
    either = "ei"

    optionFlag = (
        (must, '必修'),
        (choice, '选修'),
        (either, '任选'),
        ("ot", "其他"),
    )

    SchoolYearID = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE, verbose_name="学年ID")
    # SchoolYear = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    LessonID = models.ForeignKey("LessonInfo", on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="学分")
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="成绩")
    ifRestudied = models.BooleanField(default=True)
    testKind = models.CharField(choices=testFlag, max_length=2, default=passed, verbose_name="考试性质")
    optionChoice = models.CharField(choices=optionFlag, max_length=2, default=must, verbose_name="课程性质")


class LessonInfo(models.Model):  # 课程信息
    byTest = "bt"
    byElse = "bl"

    examFlag = (
        (byElse, '考察'),
        (byTest, '考核')
    )

    commonBase = "cb"
    pe = "pe"
    professional = "pf"
    commonChoose = "cc"
    classBase = "lb"
    educationBase = "eb"
    platformBase = "fb"
    practiceState = "ps"
    extendEnglish = "ee"
    professionalBase = "pb"
    societyCertify = "sc"
    unClassified = "uc"
    commonMust = "cm"
    optional = "op"
    professionalMust = "pm"
    professionalOption = "po"
    others = "ot"

    classifications = (
        (commonBase, '公共基础'),
        (pe, '体育'),
        (societyCertify, '证书'),
        (others, '其他'),
        (commonMust, '公共必修'),
        (unClassified, '未分类'),
        (optional, '选修'),
        (professional, '专业'),
        (professionalMust, '专业必修'),
        (professionalOption, '专业选修'),
        (professionalBase, '专业基础'),
        (commonChoose, '校公选课'),
        (classBase, '大类基础'),
        (educationBase, '基础教育'),
        (platformBase, '平台基础'),
        (practiceState, '实践环节'),
        (extendEnglish, '扩展英语'),
    )

    lessonName = models.CharField(max_length=25, verbose_name="课程名称")
    examineFlag = models.CharField(choices=examFlag, max_length=2, default=byTest, verbose_name="考查方式")
    classification = models.CharField(choices=classifications, max_length=2, default=commonBase, verbose_name="课程类别")
    AffiliatedMajor = models.ManyToManyField("MajorInfo", verbose_name="隶属专业")
    credit = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="学分")
    # timePeriod = models.DurationField(blank=True, null=True, verbose_name="开课时间")
    SchoolYearID = models.ForeignKey("SchoolYearInfo", on_delete=models.CASCADE, verbose_name="学年信息")
    lessonClass = models.IntegerField(default=0, verbose_name="本科生/研究生")


class MajorInfo(models.Model):  # 专业信息
    semesterChoices = (
        ("0", '上'),
        ("1", '下')
    )

    underYear = (
        ("01", "大一"),
        ("02", "大二"),
        ("03", "大三"),
        ("04", "大四"),

        ("11", "研一"),
        ("12", "研二"),
        ("13", "研三")
    )

    majorName = models.CharField(max_length=25, verbose_name="专业名称")
    DeptID = models.ForeignKey(DeptInfo, on_delete=models.CASCADE, verbose_name="隶属学院")
    isPostgraduate = models.BooleanField(default=False, verbose_name="本科生/研究生")
    studentNum = models.IntegerField(default=0, verbose_name="学生人数")
    SchoolYearID = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE, verbose_name="学年信息")
    underyear = models.CharField(choices=underYear, max_length=2, verbose_name="年级")
    semesterChoice = models.CharField(choices=semesterChoices, max_length=1, default="0", verbose_name="学期")
    Members = models.ManyToManyField(User, through="Relationship", verbose_name="专业关系")


# class ExtendMajorInfo(BaseModel):
#     semesterChoices = (
#         ("0", '上'),
#         ("1", '下')
#     )
#
#     underYear = (
#         ("01", "大一"),
#         ("02", "大二"),
#         ("03", "大三"),
#         ("04", "大四"),
#
#         ("11", "研一"),
#         ("12", "研二"),
#         ("13", "研三")
#     )
#
#     MajorInfo = models.ForeignKey(MajorInfo, on_delete=models.CASCADE)
#

# TODO
class Relationship(models.Model):  # 关联信息
    postGraduate = "pg"
    underGraduate = "ug"
    graduated = "gd"
    quitted = "qd"
    delayed = "dl"

    relationship = (
        (postGraduate, '研究生'),
        (underGraduate, '本科生'),
        (graduated, "已毕业"),
        (quitted, "已退学/延期毕业"),
        (delayed, "休学")
    )

    underYear = (
        ("01", "大一"),
        ("02", "大二"),
        ("03", "大三"),
        ("04", "大四"),

        ("11", "研一"),
        ("12", "研二"),
        ("13", "研三")
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Majority = models.ForeignKey(MajorInfo, on_delete=models.CASCADE)
    # ExtendMajor = models.ForeignKey(ExtendMajorInfo, on_delete=models.CASCADE)
    SchoolYearInfo = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE, null=True, blank=True)
    startDate = models.DateField(verbose_name="起始日期")
    endDate = models.DateField(default=9999 - 12 - 31, verbose_name="终止日期")
    relation = models.CharField(choices=relationship, max_length=2, default='ug', verbose_name="学生类型")
    underYear = models.CharField(choices=underYear, max_length=2, default="01", verbose_name="学生年级")
