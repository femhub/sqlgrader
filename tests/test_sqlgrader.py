import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import sqlite3
from sqlgrader import *

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

def run_sql(sql_statement, conn=None):
    """
    Execute an SQL statement against a database connection and return the results.
    
    Args:
        sql_statement: SQL statement to execute (string or sqlparse.sql.Statement)
        conn: SQLite connection (optional, uses a new in-memory DB if not provided)
        
    Returns:
        dict with 'columns' and 'rows' keys
    """
    # Convert sqlparse.sql.Statement to string if needed
    if not isinstance(sql_statement, str):
        sql_statement = str(sql_statement)
    
    # Create a new connection if none provided
    close_conn = False
    if conn is None:
        conn, _ = setup_test_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    
    # Get column names from cursor description
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Close connection if we created it
    if close_conn:
        conn.close()
    
    return {
        "columns": columns,
        "rows": rows
    }

def grade_message(result, message = ''):
    if message == '':
        message = 'Total grading result'
    if result:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def grade(grader, prefix = ''):
    if grader: # If False is returned grader found no problems
        if isinstance(grader, list):
            for i in grader:
                grade_message(i[0], prefix + i[1])
            all_positive = not [True for i in grader if i[0] != True]
            if not all_positive:
                grade_message(False)
                return False
        elif isinstance(grader, str):
            grade_message(False, prefix + grader)
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
    
    sol_code = sql_clean_and_divide(sol_code_str)
    student_code = sql_clean_and_divide(student_code_str)
    
    # Handler
    def select_1(sol_st, student_st):
        sol_res = run_sql(sol_st, conn)
        student_res = run_sql(student_st, conn)
        
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
    
    # If we got here, the test passed
    assert True
    
def test_incorrect_query(test_db):
    conn, _ = test_db

    # Get student and solution codes
    sol_code_str     = "SELECT name FROM students WHERE grade > 80"
    student_code_str = "SELECT name FROM students WHERE grade > 89"
    
    sol_code = sql_clean_and_divide(sol_code_str)
    student_code = sql_clean_and_divide(student_code_str)
    
    # Handler
    def select_1(sol_st, student_st):
        sol_res = run_sql(sol_st, conn)
        student_res = run_sql(student_st, conn)
        
        if not grade(sql_select_grader(sol_st, student_st, sol_res, student_res)):
            return False
        return True
    
    # Grading
    global_grader = sql_global_grader_opt(sol_code, student_code)
    if not grade(global_grader):
        assert False
    
    # Only the select handler is present
    if not select_1(sol_code[0], student_code[0]):
        assert True
        return
    
    # If we got here, the test passed
    assert False
