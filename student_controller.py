import connexion
from flask import current_app
from swagger_server.models.student import Student  # noqa: E501
from swagger_server.models.student_input import StudentInput  # noqa: E501
from swagger_server.models.student_response import StudentResponse  # noqa: E501

def students_get():  # noqa: E501
    """Retrieve all students"""
    manager = current_app.config['STUDENT_MANAGER']  # Access StudentManager
    students = manager.getAllStudents()
    return [student.to_dict() for student in students], 200


def students_id_delete(id_):  # noqa: E501
    """Delete a student by ID"""
    manager = current_app.config['STUDENT_MANAGER']
    try:
        manager.deleteStudent(id_)
        return {"message": "Student deleted successfully"}, 200
    except KeyError as e:
        return {"message": str(e)}, 404


def students_id_put(body, id_):  # noqa: E501
    """Update an existing student by ID"""
    manager = current_app.config['STUDENT_MANAGER']
    if connexion.request.is_json:
        updated_data = StudentInput.from_dict(connexion.request.get_json())
        updated_student = Student(
            id=None,
            name=updated_data.name,
            age=updated_data.age,
            email=updated_data.email,
            course=updated_data.course
        )
        try:
            student = manager.updateStudent(id_, updated_student)
            return student, 200
        except KeyError as e:
            return {"message": str(e)}, 404


def students_post(body):  # noqa: E501
    """Add a new student"""
    manager = current_app.config['STUDENT_MANAGER']
    if connexion.request.is_json:
        student_data = StudentInput.from_dict(connexion.request.get_json())
        new_student = Student(
            id=None,  # ID will be set in the manager
            name=student_data.name,
            age=student_data.age,
            email=student_data.email,
            course=student_data.course
        )
        added_student = manager.addStudent(new_student)
        return added_student, 201
