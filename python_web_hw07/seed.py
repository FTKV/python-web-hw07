import asyncio
from datetime import date, timedelta
from math import floor
from random import randint, choice, sample, shuffle
import string

import faker

from connect_db import AsyncDBSession
from models import Course, Grade, Group, Lecturer, Student


NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_LECTURERS = 5
NUMBER_COURSES = 8
APPROX_NUMBER_GRADES = 1000
COURSES = set(["Фізика", "Математика", "Українська мова", "Англійська мова", "Історія України", "Всесвітня історія", "Українська література", "Хімія"])


fake_data = faker.Faker("uk_UA")


async def get_fake_group():
    for _ in range(NUMBER_GROUPS):
        yield f"{''.join([choice(string.ascii_uppercase) for _ in range(3)])}-{''.join(choice(string.digits) for _ in range(3))}"


async def get_fake_student():
    for _ in range(NUMBER_STUDENTS):
        yield (lambda x: (x[1], x[2], randint(1, NUMBER_GROUPS)) if len(x) == 3 else (x[0], x[1], randint(1, NUMBER_GROUPS)))(fake_data.name().split(" "))


async def get_fake_lecturer():
    for _ in range(NUMBER_LECTURERS):
        yield (lambda x: (x[1], x[2]) if len(x) == 3 else (x[0], x[1]))(fake_data.name().split(" "))


async def get_fake_course():
    courses = list(COURSES)
    shuffle(courses)
    for i in range(len(courses)):
        yield (courses[i], randint(1, NUMBER_LECTURERS))


async def get_fake_grade():
    n = 0
    lesson_date = date(2022, 9, 1)
    while n < APPROX_NUMBER_GRADES:
        lesson_date += timedelta(days=randint(0, 3))
        course_id = randint(1, NUMBER_COURSES)
        number_of_students = randint(floor(0.8*NUMBER_STUDENTS), NUMBER_STUDENTS)
        n += number_of_students
        student_ids = sample(range(1, NUMBER_STUDENTS+1), k=number_of_students)
        for student_id in student_ids:
            yield (lesson_date, randint(1, 100), student_id, course_id)


async def insert_data_to_db() -> None:

    async with AsyncDBSession() as session:

        async for title in get_fake_group():
            group = Group(title=title)
            session.add(group)

        async for first_name, last_name, group_id in get_fake_student():
            student = Student(first_name=first_name, last_name=last_name, group_id=group_id)
            session.add(student)

        async for first_name, last_name in get_fake_lecturer():
            lecturer = Lecturer(first_name=first_name, last_name=last_name)
            session.add(lecturer)

        async for title, lecturer_id in get_fake_course():
            course = Course(title=title, lecturer_id=lecturer_id)
            session.add(course)

        async for lesson_date, grade, student_id, course_id in get_fake_grade():
            grade = Grade(lesson_date=lesson_date, grade=grade, student_id=student_id, course_id=course_id)
            session.add(grade)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(insert_data_to_db())
