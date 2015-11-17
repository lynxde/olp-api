from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from courses.models import Course, CourseSession, Event, Enrollment, EnrollmentChapter
from courses.serializer import CourseSerializer, CourseSessionSerializer


class CourseView(ViewSet):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def list(self, request, format=None):
        """
        Return a list of all courses.
        """
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        courses = Course.objects.get(id=pk)
        serializer = CourseSerializer(courses)
        return Response(serializer.data)


class CourseSessionView(ViewSet):
    """
    View for all course-sessios in system
    """

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, format=None, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        course_sessions = CourseSession.objects.filter(course_id=course_id)
        serializer = CourseSessionSerializer(course_sessions, many=True, request=request)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        course_session = CourseSession.objects.get(pk=pk)
        serializer = CourseSessionSerializer(course_session, request=request)
        return Response(serializer.data)

    @csrf_exempt
    @detail_route(methods=['get'])
    def complete_chapter(self, request, pk=None, *args, **kwargs):
        chapter_id = request.GET.get('chapter_id', None)
        course_session = CourseSession.objects.get(pk=pk)

        active_enrollment = None

        try:
            active_enrollment = Enrollment.objects.filter(course_session=course_session, user=self.request.user,
                                                          completed=False).latest('id')
        except Exception as e:
            return Response('No active enrollment for current session', status=400)

        if active_enrollment:
            enroll_chapter = EnrollmentChapter.objects.get_or_create(enrollment=active_enrollment,
                                                                     chapter_id=chapter_id)
            return Response(status=200)

        else:
            return Response('Please provide valid chapter and session', status=400)


    @csrf_exempt
    @detail_route(methods=['get'])
    def enroll(self, request, pk=None, *args, **kwargs):
        course_session = CourseSession.objects.get(pk=pk)

        active_enrollment = None

        try:
            active_enrollment = Enrollment.objects.filter(course_session=course_session, user=self.request.user,
                                                          completed=False).latest('id')
        except Exception as e:
            pass

        if active_enrollment:
            return Response('You are already enrolled', status=400)

        else:
            Enrollment(course_session=course_session, user=request.user).save()
            return Response('ok', status=200)


class EventsView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        res = []

        chapter_id = request.GET.get('chapter_id', None)

        if chapter_id:
            events = Event.objects.filter(chapter_id=chapter_id).values()

        else:
            return Response('Please provide a valid chapter id', status=400)

        return Response(events, status=200)
