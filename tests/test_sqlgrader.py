import pytest
import sqlgrader
import sqlite3

def setup_test_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE students (id INTEGER, name TEXT, grade INTEGER)")
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", [
        (1, "Alice", 85),
        (2, "Bob", 90),
    ])
    conn.commit()
    return conn, cursor

# Fixture for test database
@pytest.fixture
def test_db():
    conn, cursor = setup_test_db()
    yield conn, cursor
    conn.close()

def grade(grader, prefix = ''):
    if grader: # If False is returned grader found no problems
        if isinstance(grader, list):
            for i in grader:
                lab.grade(i[0], prefix + i[1])
            all_positive = not [True for i in grader if i[0] != True]
            if not all_positive:
                lab.grade(False)
                return False
        elif isinstance(grader, str):
            lab.grade(False, prefix + grader)
            return False
        else:
            return False # safeguard
    return True


# Test 1: Correct query matches reference
def test_correct_query(test_db):
    conn, _ = test_db

    # Get student and solution codes
    sol_code_str     = "SELECT name FROM students WHERE grade > 80"
    student_code_str = "SELECT name FROM students WHERE grade > 80"
    
    sol_code = sql_clean_and_divide(sol_code)
    student_code = sql_clean_and_divide(student_code)
    
    # Handler
    def select_1(sol_st, student_st):
        sol_res = run_sql(sol_st)
        student_res = run_sql(student_st)
        
        if not grade(sql_select_grader(sol_st, student_st, sol_res, student_res)):
            return False
        return True
    
    # Grading
    global_grader = sql_global_grader_opt(sol_code, student_code)
    if not grade(global_grader):
        return False
    
    # Only the select handler is present
    if not select_1(sol_code[0], student_code[0]):
        return False
    
