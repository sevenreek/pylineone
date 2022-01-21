from curses.ascii import HT
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from codeedit.models import Task
from utils import get_mongo_client, run_script, get_detached_container, is_code_multi_line
import ast
import docker
import docker.errors
import uuid
import os
def list_tasks(request):
    mongo, mdb = get_mongo_client()
    tasks = list(mdb['tasks'].find())
    for t in tasks:
        t['id'] = t['_id']
    return render(request, 'list.html', {
        'tasks': tasks
    })

def show_task(request, task_id):
    if not request.session.session_key:
        request.session.create()

    print(request.session.session_key)
    mongo, mdb = get_mongo_client()
    task = mdb['tasks'].find_one({"_id":task_id})
    task_details = mdb['task_details'].find_one({"task_id":task_id})
    task_tests = mdb['tests'].find({"task_id":task_id})
    task = {**task, **task_details, 'id':task['_id']}
    print(task)
    return render(request, 'editor.html', {
        "task":task,
        "tests":task_tests
    })

def check_task(request, task_id):
    client = docker.from_env()
    code = request.body.decode("utf-8")
    if is_code_multi_line(code):
        return HttpResponse("Your code contains semicolons or newline characters outside strings.", status=400)
    mongo, mdb = get_mongo_client()
    task = mdb['task_details'].find_one({"task_id":task_id})
    task_tests = mdb['tests'].find({"task_id":task_id})
    filename = f"{uuid.uuid4().hex}.py"
    filepath = os.path.join(os.path.abspath(os.getcwd()), filename)
    function_code = f"def {task['function_name']}({','.join(task['input_arguments'])}): return {code}\n"
    expected_output = []
    with open(filename, 'w') as script_file:
        script_file.write(function_code)
        for test in task_tests:
            positionals = ", ".join(test['input_positional'])
            test_code = f"print({task['function_name']}({positionals}))\n"
            script_file.write(test_code)
            expected_output.append(test['output'])
    try:
        result = client.containers.run(
            'python', 
            f'python3 {filename}', 
            remove=True, 
            volumes=[f"{filepath}:/home/{filename}"],
            working_dir='/home'
        )
    except docker.errors.ContainerError:
        return HttpResponse("Your code is not proper Python code.", status=400)
    finally:
        os.remove(filename)

    print(expected_output)
    results = result.decode("utf-8").split("\n")
    results = results[:-1] # remove last empty line
    print(results)
    successes = [e==o for e,o in zip(expected_output, results)]
    print(successes)
    response = JsonResponse({'proper_code':True, 'test_results':successes, 'return_values':results})
    if all(successes):
        response.set_cookie(f"task{task_id}", "solved", max_age=3600*24*365) # expire in a year
    else:
        response.set_cookie(f"task{task_id}", "attempted", max_age=3600*24*365) # expire in a year
    response.set_cookie(f"task{task_id}_attempt", code, max_age=3600*24*365) # expire in a year
    
    return response
    

def run_test(request, task_id, test_id):
    pass
# Create your views here.
