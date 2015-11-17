from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class Course(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "{0}".format(self.name)


class Section(TimeStampedModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name="sections")

    def __unicode__(self):
        return "{0} : {1}".format(self.name, self.course)


class Chapter(TimeStampedModel):
    CHAPTER_TYPES = (
        ('quiz', 'quiz'),
        ('text', 'text'),
        ('webinar', 'webinar'),
    )
    section = models.ForeignKey(Section, related_name="chapters", default=None, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=CHAPTER_TYPES)
    expected_min = models.IntegerField()

    def __unicode__(self):
        return "{0} : {1}".format(self.name, self.section)


class CourseSession(TimeStampedModel):
    course = models.ForeignKey(Course, related_name="sessions")
    start_time = models.DateTimeField()
    users = models.ManyToManyField(User, related_name='enrollments', through="Enrollment")

    def __unicode__(self):
        return "{0} : session {1}".format(self.course, self.start_time)


class Enrollment(models.Model):
    user = models.ForeignKey(User)
    course_session = models.ForeignKey(CourseSession)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return "Enrollment : {0}-{1}".format(self.user, self.course_session)


class EnrollmentChapter(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="chapter_enrollment")
    enrollment = models.ForeignKey(Enrollment, related_name="enrollment_enrollment")

    def __unicode__(self):
        return "{0} : {1}".format(self.chapter, self.enrollment)

    class Meta:
        unique_together = ('chapter', 'enrollment')


class Event(TimeStampedModel):
    chapter = models.ForeignKey(Chapter, related_name="events")
    date_time = models.DateTimeField()
    link = models.URLField()

    def __unicode__(self):
        return "{0} : {1}".format(self.chapter, self.date_time)