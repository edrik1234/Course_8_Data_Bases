from swagger_server.models.student import Student 
import sqlalchemy
import config
import json
class StudentManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(config.DATABASE_URL)
        self.students = {}
        self.current_id = 1

    def getAllStudents(self) -> list[Student]:
        """Retrieve all students as a list."""
        my_query = """ 
            SELECT * FROM """ + config.DB_TABLE_NAME
        students = []
        with self.engine.connect() as connection:
            result = connection.execute(
                sqlalchemy.text(my_query) ,
            )
          #  for row in result:
            return[Student(row[0], row[1], row[2], row[3], "no_course") for row in result ]
                #students.append(student)
        #return students

    #def getStudentById(self, student_id: int) -> list[Student]:
       # return self.students.get(student_id)

    def addStudent(self, student: Student) -> str:
        my_query = f"""INSERT INTO  {config.DB_TABLE_NAME}(name, age, email) VALUES
        (:name , :age , :email)
        RETURNING row_to_json(""" + config.DB_TABLE_NAME + """)
        """
        with self.engine.connect() as connection:
            transaction = connection.begin() # get ready changes will come
            #used when we do changes like: create , update and delete
            result = connection.execute(
            sqlalchemy.text(my_query) ,
            {"name": student.name, "age": student.age, "email": student.email}
        )
            output = result.fetchone()[0]
            transaction.commit()# the changes are save as in git , to prevent unupdating the table of students
            #used whhen we do changes like: crete , update and delete
        return output

    def updateStudent(self, student_id: int, updated_student: Student) -> Student:
        my_query = f"""UPDATE Students 
        SET  age = :age , name = :name  , email = :email 
        WHERE id = :id
        RETURNING row_to_json(Students)
        """
        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
            sqlalchemy.text(my_query) ,
            {"name": updated_student.name, "age": updated_student.age, "email": updated_student.email, "id" : student_id}
            )
            output = result.fetchone()
            transaction.commit()
        if output == None:
                raise KeyError
        json_data = output[0]
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        return json_data  # מחזיר dict אמיתי ל-Flask
     

        #if student_id in self.students:
           # updated_student.id = student_id  # Preserve the ID
           # self.students[student_id] = updated_student  # Replace the student entry
           # return updated_student

    def deleteStudent(self, student_id: int) -> None:
        my_query = f""" DELETE FROM {config.DB_TABLE_NAME} 
        WHERE id = :id
        RETURNING id
        """
        with self.engine.connect() as connection:
            transaction = connection.begin() # get ready changes will come
            #used when we do changes like: create , update and delete
            result = connection.execute(
            sqlalchemy.text(my_query) ,
            {"id": student_id}
            )
            transaction.commit()# the changes are save as in git , to prevent unupdating the table of students
            #used whhen we do changes like: crete , update and delete
            #del self.students[student_id]
            # Remove student from the dictionary
            if result.scalar() == None:
                raise KeyError