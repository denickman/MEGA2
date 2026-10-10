import pytest




class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.years = years
        self.major = major




@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Math", 2)



def test_person_init(default_employee):
    # p = Student("John", "Doe", major="Math", years=2)
    assert default_employee.first_name == "John", "first name should be 'John'"
    assert default_employee.last_name == "Doe", "last name should be 'Doe'"
    assert default_employee.major == "Math", "major should be 'Math'"
    assert default_employee.years == 2, "years should be 2'"


