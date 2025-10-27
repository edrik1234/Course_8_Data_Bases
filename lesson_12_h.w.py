import sqlalchemy
USERNAME = "username"
PASSWORD = "password"
DB_HOSTNAME = "localhost"
DB_NAME = "college"

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{DB_HOSTNAME}/{DB_NAME}"
engine = sqlalchemy.create_engine(DATABASE_URL)# i will use sql alchemy in order to connect to data base using sql alchemy object, his name is engine like in flask(app)

# in order to do a line drop i do a 3 quotation marks in each side like here:



def print_number_of_students_in_table():
    my_query = """ 
    SELECT COUNT(*) AS total_rows FROM Students
"""

    with engine.connect() as connection:
        result = connection.execute(
        sqlalchemy.text(my_query) 
        )
        print(result.scalar())    


def print_average_ages():
    my_query = """ 
    SELECT AVG(age) AS total_ages FROM Students
"""

    with engine.connect() as connection:
        result = connection.execute(
        sqlalchemy.text(my_query) 
        )    
        print(result.scalar()) 




def insert_a_new_student():
    with engine.connect() as connection:
        my_query = """ 
        INSERT INTO Students(name, age, email) 
        VALUES  (:name , :age , :email)
        RETURNING id
        """
        name = input("please enter name: ")
        age = int((input("please enter age: ")))
        email = input("please enter email: ")
        transaction = connection.begin()
        result = connection.execute(
            sqlalchemy.text(my_query) ,
            {"name": name , "age": age, "email": email}
            )
        transaction.commit()
        print(f"Inserted new student with ID: {result.scalar()}")


def print_all_students():
      with engine.connect() as connection:
        my_query = """ 
            SELECT * FROM Students
        """
        result = connection.execute(
            sqlalchemy.text(my_query)
        )
        for row in result:
            print(row)

def menu():
    while True:
        print("\n========= MENU =========")
        print("1)  Show total number of students")
        print("2️)  Show average age of students")
        print("3️)  Add a new student")
        print("4️)  Show all students")
        print("5️) Exit")
        print("========================")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            print_number_of_students_in_table()
        elif choice == "2":
            print_average_ages()
        elif choice == "3":
            insert_a_new_student()
        elif choice == "4":
            print_all_students()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print(f"invalid choice please try again")
        

if __name__ == "__main__":
    menu()