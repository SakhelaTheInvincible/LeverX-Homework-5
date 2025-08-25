import factory
from django.contrib.auth import get_user_model
from courses.models import Course, Lecture
from homework.models import HomeworkAssignment, HomeworkSubmission, Grade


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = get_user_model()

	username = factory.Sequence(lambda n: f"user{n}")
	first_name = "Test"
	last_name = factory.Sequence(lambda n: f"User{n}")
	email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
	role = "student"

	@factory.post_generation
	def password(obj, create, extracted, **kwargs):
		pw = extracted or "passw0rd!"
		obj.set_password(pw)
		if create:
			obj.save()


class TeacherFactory(UserFactory):
	role = "teacher"


class CourseFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Course

	name = factory.Sequence(lambda n: f"Course {n}")
	description = factory.Faker("sentence")
	owner = factory.SubFactory(TeacherFactory)

	@factory.post_generation
	def add_owner_as_teacher(obj, create, extracted, **kwargs):
		if create and obj.owner_id:
			obj.teachers.add(obj.owner)


class LectureFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Lecture

	course = factory.SubFactory(CourseFactory)
	topic = factory.Sequence(lambda n: f"Lecture {n}")


class HomeworkAssignmentFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = HomeworkAssignment

	lecture = factory.SubFactory(LectureFactory)
	text = factory.Faker("paragraph")


class HomeworkSubmissionFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = HomeworkSubmission

	assignment = factory.SubFactory(HomeworkAssignmentFactory)
	student = factory.SubFactory(UserFactory)
	answer_text = factory.Faker("paragraph")


class GradeFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Grade

	submission = factory.SubFactory(HomeworkSubmissionFactory)
	graded_by = factory.SubFactory(TeacherFactory)
	score = 5
	comment = factory.Faker("sentence")


