from django.db import models
from apps.account.models import User
from apps.award_info.models import AwardInfo
from apps.grade_info.models import SchoolYearInfo
from database.base_model import BaseModel


# Create your models here.


class AwardHistory(models.Model):
    User = models.ManyToManyField(User)
    awardName = models.CharField(max_length=25, verbose_name="奖学金名称")
    AwardID = models.ForeignKey(AwardInfo, on_delete=models.CASCADE)
    AwardYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE, verbose_name="获奖学年")


"""
    论文发表
"""


class PaperRecord(models.Model):
    first = "f"
    second = "s"
    third = "t"
    fourth = "r"
    others = "o"

    orderChoice = (
        (first, "第一作者"),
        (second, "第二作者"),
        (third, "第三作者"),
        (fourth, "共同第一作者"),
        (others, "其它")
    )

    postOnline = "po"
    postAlready = "pa"

    postState = (
        (postOnline, '在线发表'),
        (postAlready, '正式发表'),
        ('ot', '其它')
    )

    conferenceTitle = (
        ("ic", "国际会议"),
        ("im", "重要期刊"),
        ("tm", "顶级期刊"),
        ("os", "其它SCI期刊"),
        ("om", "国际期刊"),
        ("nm", "国内期刊"),
        ("nc", "国内会议"),
        ("ot", "其它")
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    publishDate = models.DateField(verbose_name="发表日期")
    name = models.CharField(max_length=256, verbose_name="论文名称")
    abstract = models.TextField(null=True, blank=True, verbose_name="摘要")
    magzineName = models.CharField(verbose_name="期刊名称", max_length=256, null=True, blank=True)
    authOrder = models.CharField(choices=orderChoice, max_length=1, default=first, verbose_name="作者顺序")
    totalAuthor = models.IntegerField(default=2, verbose_name="作者人数")
    postStatus = models.CharField(choices=postState, max_length=2, default=postAlready, verbose_name="发表状态")
    totalReference = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name="他引状况")
    conferenceChoice = models.CharField(choices=conferenceTitle, max_length=2, default="ot", verbose_name="期刊等级")


"""
    发明专利
"""


class PatentRecord(models.Model):
    inventP = "ip"

    patentTypeChoices = (
        (inventP, "发明专利"),
        ("ot", "其它")
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name="专利名称")
    classify = models.CharField(choices=patentTypeChoices, max_length=2, verbose_name="专利类别", default=inventP)
    applyNumber = models.CharField(max_length=25, verbose_name="专利申请号")
    applyTime = models.DateField(verbose_name="专利申请日期")
    certificateNumber = models.CharField(max_length=25, null=True, blank=True, verbose_name="专利证书编号")
    approveDate = models.DateField(null=True, blank=True, verbose_name="专利批准日期")
    holdUnit = models.CharField(max_length=25, verbose_name="专利持有单位")


"""
    出版专著
"""


class PublishRecord(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name="著作名称")
    publishing_house = models.CharField(max_length=256, verbose_name="出版社")
    contribution = models.CharField(max_length=256, verbose_name="工作量")
    bookKey = models.CharField(max_length=256, verbose_name="书号")
    publish_date = models.DateField(verbose_name="出版日期")
    publishType = models.CharField(max_length=256, verbose_name="编著类型")
    authorAmount = models.IntegerField(default=1, verbose_name="作者人数")
    authorNum = models.IntegerField(default=1, verbose_name="第几作者")


"""
    科研获奖
    创新竞赛
"""


class CompetitionRecord(models.Model):
    national = "na"
    international = "in"
    district = "ds"
    localRange = "lr"
    collegeRange = "cl"

    competitionRange = (
        (national, "全国"),
        (international, "国际"),
        (district, "省市/区域"),
        (localRange, "校级"),
        (collegeRange, "学院"),
        ("ot", "其它")
    )

    super = "u"
    first = "f"
    second = "s"
    third = "t"
    fourth = "r"
    others = "o"

    awardRange = (
        (super, "特等奖"),
        (first, "一等奖"),
        (second, "二等奖"),
        (third, "三等奖"),
        (fourth, "四等奖"),
        (others, "其他"),
    )

    researchAward = "ra"
    innoveAward = "ia"

    awardType = (
        (researchAward, '科技获奖'),
        (innoveAward, '创新竞赛')
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="竞赛名称", max_length=256)
    holder = models.CharField(verbose_name="主办单位", max_length=256)
    awardName = models.CharField(max_length=25, verbose_name="奖项名称")
    competeRange = models.CharField(choices=competitionRange, max_length=2, default=national, verbose_name="获奖级别")
    awardLevel = models.CharField(choices=awardRange, max_length=1, default=first, verbose_name="本人获奖等级")
    otherAward = models.CharField(null=True, max_length=256, blank=True, verbose_name="其他获奖等级")
    teammateAmount = models.IntegerField(default=1, verbose_name="团队人数")
    selfOrder = models.IntegerField(default=1, verbose_name="本人第几")
    certificateID = models.CharField(verbose_name="获奖证书编号", max_length=256, blank=True, null=True)
    certificateDistributeOrganizationName = models.CharField(verbose_name="获奖证书颁发单位", max_length=256, blank=True,
                                                             null=True)
    type = models.CharField(choices=awardType, default=innoveAward, max_length=2, verbose_name="(科技创新/竞赛)")


"""
    科研项目
"""


class ResearchProject(models.Model):
    others = "ot"
    nationalNatureFundSurf = "ns"
    nationalNatureFundImport = "nm"
    nationalNatureFundOthers = "no"
    nationalNatureFundGreat = "ng"
    defenseTechFundImport = "dm"
    Project973 = "p9"
    Project863 = "p8"

    projectChoice = (
        (nationalNatureFundSurf, "国家自然科学基金面上项目"),
        (nationalNatureFundOthers, "国家自然科学基金其他项目"),
        (nationalNatureFundImport, "国家自然科学基金重要项目"),
        (nationalNatureFundGreat, "国家自然科学基金重大项目"),
        (defenseTechFundImport, "国防科技重点实验基金项目"),
        (Project973, "973项目"),
        (Project863, "863项目"),
        (others, "其他")
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYearInfo = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name="项目名称")
    projectType = models.CharField(choices=projectChoice, max_length=2, default=others, verbose_name="项目类型")
    projectWork = models.CharField(max_length=256, verbose_name="工作任务")


"""
    荣誉称号
    其他成果
"""


class HonorTitle(models.Model):
    others = "ot"
    academy = "ac"
    college = "co"
    national = "na"
    international = "in"
    district = "ds"

    honorRankChoice = (
        (international, "国际级"),
        (academy, "学院级"),
        (district, "省部级"),
        (college, "学校级"),
        (national, "国家级"),
        (others, "其他")
    )

    honorChoice = (
        ("ho", "荣誉称号"),
        ("ot", "其他成果")
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    honorName = models.CharField(max_length=25, verbose_name="荣誉名称")
    proclaimOrganization = models.CharField(max_length=25, verbose_name="颁发单位")
    honorRank = models.CharField(choices=honorRankChoice, max_length=2, default=academy, verbose_name="荣誉级别")
    issueDate = models.DateField(verbose_name="获得日期")
    type = models.CharField(choices=honorChoice, default="ho", max_length=2, verbose_name="荣誉称号/其他成果")
