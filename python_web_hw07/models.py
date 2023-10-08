import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, CheckConstraint, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(79), nullable=False, unique=True)
    students: Mapped['Student'] = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(79), nullable=False)
    last_name: Mapped[str] = mapped_column(String(79), nullable=False)
    group_id: Mapped[int] = mapped_column('group_id', Integer, ForeignKey('groups.id', onupdate="CASCADE"))
    group: Mapped['Group'] = relationship("Group", back_populates="students")
    grades: Mapped['Grade'] = relationship("Grade", back_populates="student")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Lecturer(Base):
    __tablename__ = 'lecturers'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(79), nullable=False)
    last_name: Mapped[str] = mapped_column(String(79), nullable=False)
    courses: Mapped['Course'] = relationship("Course", back_populates="lecturer")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(79), nullable=False, unique=True)
    lecturer_id: Mapped[int] = mapped_column('lecturer_id', Integer, ForeignKey('lecturers.id', ondelete="SET NULL", onupdate="CASCADE"))
    lecturer: Mapped['Lecturer'] = relationship("Lecturer", back_populates="courses")
    grades: Mapped['Grade'] = relationship("Grade", back_populates="course")


class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    grade: Mapped[int] = mapped_column(Integer, CheckConstraint("grade >= 1 and grade <= 100"), nullable=True)
    student_id: Mapped[int] = mapped_column('student_id', Integer, ForeignKey('students.id', ondelete="CASCADE", onupdate="CASCADE"))
    course_id: Mapped[int] = mapped_column('course_id', Integer, ForeignKey('courses.id', ondelete="CASCADE", onupdate="CASCADE"))
    student: Mapped['Student'] = relationship("Student", back_populates="grades")
    course: Mapped['Course'] = relationship("Course", back_populates="grades")
