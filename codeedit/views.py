from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from codeedit.models import Task
from utils import get_mongo_client, run_script, get_detached_container
import ast
import docker
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
    mongo, mdb = get_mongo_client()
    task = mdb['tasks'].find_one({"_id":task_id})
    task_details = mdb['task_details'].find_one({"task_id":task_id})
    task_tests = mdb['tests'].find({"task_id":task_id})
    task = {**task, **task_details}
    print(task)
    return render(request, 'editor.html', {
        "task":task,
        "tests":task_tests
    })

def check_task(request, task_id):
    client = docker.from_env()
    code = request.body.decode("utf-8")
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
    result = client.containers.run(
        'python', 
        f'python3 {filename}', 
        remove=True, 
        volumes=[f"{filepath}:/home/{filename}"],
        working_dir='/home'
    )
    print(expected_output)
    results = result.decode("utf-8").split("\n")
    print(results)
    successes = [e==o for e,o in zip(expected_output, results)]
    print(successes)
    os.remove(filename)
    return JsonResponse({'test_results':successes, 'return_values':results})

def run_test(request, task_id, test_id):
    pass
# Create your views here.
