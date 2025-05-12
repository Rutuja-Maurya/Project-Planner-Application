from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from concrete_implementation import User, Team, ProjectBoard
import json

# Initialize our managers
user_manager = User()
team_manager = Team()
board_manager = ProjectBoard()

def home(request):
    """Home view that displays the main dashboard"""
    return render(request, 'home.html')

# User views
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            response = user_manager.create_user(request.body.decode())
            user_data = json.loads(response)
            if 'error' in user_data:
                return JsonResponse({'error': user_data['error']}, status=400)
            return JsonResponse(user_data)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON response'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_users(request):
    try:
        response = user_manager.list_users()
        users = json.loads(response)
        if request.method == 'GET':
            return render(request, 'users/list.html', {'users': users})
        elif request.method == 'POST':
            return JsonResponse(users, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def describe_user(request):
    if request.method == 'POST':
        try:
            response = user_manager.describe_user(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        try:
            response = user_manager.update_user(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_user_teams(request):
    if request.method == 'POST':
        try:
            response = user_manager.get_user_teams(request.body.decode())
            return JsonResponse(json.loads(response), safe=False)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        try:
            response = user_manager.delete_user(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Team views
@csrf_exempt
def create_team(request):
    if request.method == 'POST':
        try:
            response = team_manager.create_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_teams(request):
    try:
        response = team_manager.list_teams()
        teams = json.loads(response)
        if request.method == 'GET':
            return render(request, 'teams/list.html', {'teams': teams})
        elif request.method == 'POST':
            return JsonResponse(teams, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def describe_team(request):
    if request.method == 'POST':
        try:
            response = team_manager.describe_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_team(request):
    if request.method == 'PUT':
        try:
            response = team_manager.update_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def add_users_to_team(request):
    if request.method == 'POST':
        try:
            response = team_manager.add_users_to_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def remove_users_from_team(request):
    if request.method == 'POST':
        try:
            response = team_manager.remove_users_from_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_team_users(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            team_id = data.get('team_id')
            board_id = data.get('id')  # For backward compatibility with board requests

            # If board_id is provided, get team_id from the board
            if board_id and not team_id:
                boards = board_manager._load_boards()
                board = next((b for b in boards if b['id'] == board_id), None)
                if not board:
                    raise ValueError("Board not found")
                team_id = board['team_id']
            
            if not team_id:
                raise ValueError("Team ID is required")

            # Get team users
            response = team_manager.list_team_users(json.dumps({'id': team_id}))
            users = json.loads(response)
            
            return JsonResponse(users, safe=False)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_team(request):
    if request.method == 'DELETE':
        try:
            response = team_manager.delete_team(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Board views
@csrf_exempt
def create_board(request):
    if request.method == 'POST':
        try:
            response = board_manager.create_board(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def close_board(request):
    if request.method == 'POST':
        try:
            response = board_manager.close_board(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        try:
            response = board_manager.add_task(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_task_status(request):
    if request.method == 'PUT':
        try:
            response = board_manager.update_task_status(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_boards(request):
    try:
        if request.method in ['GET', 'POST']:
            # For GET requests, we'll list all boards
            # For POST requests, we'll list boards for a specific team
            if request.method == 'GET':
                boards = board_manager._load_boards()
                # Get user details for task assignments
                users = {u['id']: u['display_name'] for u in user_manager._load_users()}
                
                result_boards = []
                for board in boards:
                    total_tasks = len(board['tasks'])
                    completed_tasks = len([t for t in board['tasks'] if t['status'] == 'COMPLETE'])
                    
                    # Enhance tasks with user display names
                    tasks = []
                    for task in board['tasks']:
                        task_copy = task.copy()
                        task_copy['assigned_to'] = users.get(task['user_id'], 'Unknown User')
                        tasks.append(task_copy)

                    result_boards.append({
                        'id': board['id'],
                        'name': board['name'],
                        'description': board['description'],
                        'status': board['status'],
                        'creation_time': board['creation_time'],
                        'tasks': tasks,
                        'total_tasks': total_tasks,
                        'completed_tasks': completed_tasks
                    })
            else:  # POST request
                response = board_manager.list_boards(request.body.decode())
                result_boards = json.loads(response)
            
            return render(request, 'boards/list.html', {'boards': result_boards})
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_board(request):
    if request.method == 'DELETE':
        try:
            response = board_manager.delete_board(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def export_board(request):
    if request.method == 'POST':
        try:
            response = board_manager.export_board(request.body.decode())
            return JsonResponse(json.loads(response))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def list_board_tasks(request):
    if request.method == 'POST':
        try:
            boards = board_manager._load_boards()
            data = json.loads(request.body.decode())
            board_id = data.get('id')
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            board = next((b for b in boards if b['id'] == board_id), None)
            if not board:
                raise ValueError("Board not found")
            
            # Get user details for task assignments
            users = {u['id']: u['display_name'] for u in user_manager._load_users()}
            
            # Enhance tasks with user display names
            tasks = []
            for task in board['tasks']:
                task_copy = task.copy()
                task_copy['assigned_to'] = users.get(task['user_id'], 'Unknown User')
                tasks.append(task_copy)
            
            return JsonResponse(tasks, safe=False)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
