from django.contrib import admin

# Register your models here.
from courses.models import Course, CourseSession, Event, Enrollment, EnrollmentChapter, Chapter, Section

admin.site.register(Course)
admin.site.register(CourseSession)
admin.site.register(Event)
admin.site.register(Enrollment)
admin.site.register(EnrollmentChapter)
admin.site.register(Chapter)
admin.site.register(Section)