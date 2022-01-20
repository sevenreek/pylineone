from pymongo import MongoClient
from models import *
from dataclasses import asdict
client= MongoClient("mongodb://admin:admin@localhost:27017")
db = client["pylineone"]
db.drop_collection('tasks')
db.drop_collection('task_details')
db.drop_collection('tests')
tasks = db["tasks"]
task_details = db["task_details"]
tests = db["tests"]

tasks_to_insert = [
    Task(0, 'Spaces to underscores', 'Replace spaces with underscores in a string.', 10, ["strings", ]),
    Task(1, 'Spaces to an underscore', 'Replace spaces with a single underscore in a string.', 15, ["strings", ]),
    Task(2, 'Unique digits', 'Count the number of unique digits in a number.', 15, ["strings", "integers", "sets"]),
    Task(3, 'Divisors', 'Calculate a number\'s dividors.', 20, ["integers", "math", "loops"]),
]
details_to_insert = [
    TaskDetails(
        0, 
        "# Write a single-line function that will replace every space character (' ')\n# in a given input string with an underscore character ('_').\n# The function should return a new string.", 
        ["# replace_spaces('say hello world!') -> 'say_hello_world!'", "# replace_spaces('say hello   world!') -> 'say_hello___world!'"],
        '',
        'spaces_to_underscores',
        ['input:str'],
        'str'
    ),
    TaskDetails(
        1, 
        "# Write a single-line function that will replace each set of space characters (' ')\n# in a given input string with a single underscore character ('_').\n# The function should return a new string.", 
        ["# replace_spaces('say hello world!') -> 'say_hello_world!'", "# replace_spaces('say hello   world!') -> 'say_hello_world!'"],
        '',
        'spaces_to_underscore',
        ['input:str'],
        'str'
    ),
    TaskDetails(
        2, 
        "# Write a single-line function that will count the number of unique digits\n# in a given input integer number.", 
        ["# count_unique_digits(123) -> 3", "# count_unique_digits(11200) -> 3"],
        '',
        'count_unique_digits',
        ['input:int'],
        'int'
    ),
    TaskDetails(
        3, 
        "# Write a single-line function that will produce a list of divisors\n# for the given input integer number.", 
        ["# divisors(8) -> [4,2,1]", "# divisors(15) -> [5,3,1]"],
        '',
        'divisors',
        ['input:int'],
        'list[int]'
    ),
]
tests_to_insert = [
    # 0
    TaskTest(
        0, 1, ['\"a a\"'], {}, 'a_a'
    ),
    TaskTest(
        0, 2, ['\"a  a\"'], {}, 'a__a'
    ),
    TaskTest(
        0, 3, ['\"a     a\"'], {}, 'a_____a'
    ),
    TaskTest(
        0, 4, ['\" \"'], {}, '_'
    ),
    TaskTest(
        0, 5, ['\"\"'], {}, ''
    ),
    TaskTest(
        0, 6, ['\" x  x \"'], {}, '_x__x_'
    ),
    # 1
    TaskTest(
        1, 1, ['\"a a\"'], {}, 'a_a'
    ),
    TaskTest(
        1, 2, ['\"a  a\"'], {}, 'a_a'
    ),
    TaskTest(
        1, 3, ['\"a     a\"'], {}, 'a_a'
    ),
    TaskTest(
        1, 4, ['\" \"'], {}, '_'
    ),
    TaskTest(
        1, 5, ['\"\"'], {}, ''
    ),
    TaskTest(
        1, 6, ['\" x  x \"'], {}, '_x_x_'
    ),
]

tasks.insert_many((asdict(o) for o in tasks_to_insert))
task_details.insert_many((asdict(o) for o in details_to_insert))
tests.insert_many((asdict(o) for o in tests_to_insert))

