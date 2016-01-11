from rest_framework.serializers import ModelSerializer
from courses.models import Course, CourseSession, Enrollment, EnrollmentChapter, Chapter, Event
from rest_framework import serializers


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        exclude = ['created', 'modified']


class CourseSessionSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CourseSessionSerializer, self).__init__(*args, **kwargs)

    active_enrollment = serializers.SerializerMethodField()
    chapter_statuses = serializers.SerializerMethodField()

    class Meta:
        model = CourseSession
        exclude = ['created', 'modified', 'users']

    def get_active_enrollment(self, obj):
        active_enrollment = Enrollment.objects.filter(course_session=obj, user=self.request.user,
                                                      completed=False).exists()
        if active_enrollment:
            return True
        else:
            return False


    def get_chapter_statuses(self, session):

        active_enrollment = None

        try:
            active_enrollment = Enrollment.objects.filter(course_session=session, user=self.request.user,
                                                          completed=False).latest('id')
        except Exception as e:
            print "No active enrollment..."

        if active_enrollment:
            chapters_completed = EnrollmentChapter.objects.filter(enrollment=active_enrollment).values_list(
                'chapter_id',
                flat=True)

            all_chapters = Chapter.objects.filter(section__in=session.course.sections.all()).values('id', 'name', 'section__name')

            for chapter in all_chapters:

                if chapter['id'] in chapters_completed:
                    chapter['completed'] = True

                else:
                    chapter['completed'] = False

            #chapter['section_name'] = chapter.section.name
                    
            #all_events = Event.objects.filter(chapter__in=Chapter.objects.filter(section__in=obj.course.sections.all()))

            return all_chapters

        else:
            return None




