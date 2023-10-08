from sqlalchemy import select, and_, desc, func, distinct

from models import Course, Grade, Group, Lecturer, Student


def select_01():
    
    stmt = (
                select(Student.full_name.label("student_full_name"), func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
                .join(Student)
                .group_by(Student.id)
                .order_by(desc("average_grade"))
                .limit(5)
            )
    
    return stmt


def select_02():

    average_grades = (
                select(Student.full_name, Course.title, func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .group_by(Student.id, Course.id)
                .subquery()
            )

    max_average_grades = (
                select(average_grades.c.title, func.max(average_grades.c.average_grade).label("max_average_grade"))
                .select_from(average_grades)
                .group_by(average_grades.c.title)
                .subquery()
            )
            
    stmt = (
                select(average_grades.c.full_name.label("student_full_name"), average_grades.c.title.label("group_title"), average_grades.c.average_grade.label("average_grade"))
                .select_from(average_grades)
                .join(max_average_grades, and_(max_average_grades.c.title == average_grades.c.title, max_average_grades.c.max_average_grade == average_grades.c.average_grade))
                .order_by(desc(average_grades.c.average_grade), average_grades.c.title)
            )
    
    return stmt


def select_03():
    
    stmt = (
                select(Group.title.label("group_title"), Course.title.label("course_title"), func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .join(Group)
                .group_by(Group.id, Course.id)
                .order_by(Group.title)
            )
    
    return stmt


def select_04():
    
    stmt = (
                select(func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
            )
    
    return stmt


def select_05():
    
    stmt = (
                select(Lecturer.full_name.label("lecturer_full_name"), func.aggregate_strings(Course.title, ", ").label("course_title_list"))
                .select_from(Lecturer)
                .join(Course)
                .group_by(Lecturer.id)
                .order_by(Lecturer.last_name)
            )
    
    return stmt


def select_06():

    stmt = (
                select(Group.title.label("group_title"), Student.full_name.label("student_full_name"))
                .select_from(Group)
                .join(Student)
                .order_by(Group.title, Student.last_name)
            )
    
    return stmt


def select_07():

    stmt = (
                select(Group.title.label("group_title"), Course.title.label("course_title"), func.array_agg(Grade.grade).label("grade_list"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .join(Group)
                .group_by(Group.id, Course.id)
                .order_by(Group.title, Course.title)
            )
    
    return stmt


def select_08():

    stmt = (
                select(Lecturer.full_name.label("lecturer_full_name"), func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
                .join(Course)
                .join(Lecturer)
                .group_by(Lecturer.id)
                .order_by(Lecturer.last_name)
            )
    
    return stmt


def select_09():

    stmt = (
                select(Student.full_name.label("student_full_name"), func.aggregate_strings(distinct(Course.title), ", ").label("course_title_list"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .group_by(Student.id)
                .order_by(Student.last_name)
            )
    
    return stmt


def select_10():

    stmt = (
                select(Lecturer.full_name.label("lecturer_full_name"), Student.full_name.label("student_full_name"), func.aggregate_strings(distinct(Course.title), ", ").label("course_title_list"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .join(Lecturer)
                .group_by(Lecturer.id, Student.id)
                .order_by(Lecturer.last_name, Student.last_name)
            )
    
    return stmt


def select_11():

    stmt = (
                select(Lecturer.full_name.label("lecturer_full_name"), Student.full_name.label("student_full_name"), func.round(func.avg(Grade.grade), 2).label("average_grade"))
                .select_from(Grade)
                .join(Student)
                .join(Course)
                .join(Lecturer)
                .group_by(Lecturer.id, Student.id)
                .order_by(Lecturer.last_name, Student.last_name)
            )
    
    return stmt


def select_12():

    last_lessons_dates = (
                select(Grade.course_id, func.max(Grade.lesson_date).label("max_lesson_date"))
                .select_from(Grade)
                .group_by(Grade.course_id)
                .subquery()
            )
            
    stmt = (
                select(Group.title.label("group_title"), Course.title.label("course_title"), last_lessons_dates.c.max_lesson_date, func.array_agg(Grade.grade).label("grade_list"))
                .select_from(last_lessons_dates)
                .join(Grade, and_(Grade.course_id == last_lessons_dates.c.course_id, Grade.lesson_date == last_lessons_dates.c.max_lesson_date))
                .join(Student)
                .join(Course)
                .join(Group)
                .group_by(Group.id, Course.id, last_lessons_dates.c.max_lesson_date)
                .order_by(Group.title, Course.title)
            )
    
    return stmt


def select_statement(user_input):
    match user_input:
        case 1:
            stmt = select_01()
        case 2:
            stmt = select_02()
        case 3:
            stmt = select_03()
        case 4:
            stmt = select_04()
        case 5:
            stmt = select_05()
        case 6:
            stmt = select_06()
        case 7:
            stmt = select_07()
        case 8:
            stmt = select_08()
        case 9:
            stmt = select_09()
        case 10:
            stmt = select_10()
        case 11:
            stmt = select_11()
        case 12:
            stmt = select_12()

    return stmt