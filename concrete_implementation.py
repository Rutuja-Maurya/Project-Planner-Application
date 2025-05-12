import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from user_base import UserBase
from team_base import TeamBase
from project_board_base import ProjectBoardBase

class User(UserBase):
    def __init__(self):
        self.db_file = os.path.join('db', 'users.json')
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        os.makedirs('db', exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def _load_users(self) -> List[Dict]:
        self._ensure_db_exists()  # Make sure the file exists
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _save_users(self, users: List[Dict]):
        with open(self.db_file, 'w') as f:
            json.dump(users, f, indent=2)

    def create_user(self, request: str) -> str:
        data = json.loads(request)
        name = data.get('name', '')
        display_name = data.get('display_name', '')

        if not name or not display_name:
            raise ValueError("Name and display_name are required")

        if len(name) > 64 or len(display_name) > 64:
            raise ValueError("Name and display_name must be max 64 characters")

        users = self._load_users()
        if any(user['name'] == name for user in users):
            raise ValueError("User name must be unique")

        # Generate sequential ID
        user_id = 1001 if not users else max(int(user['id']) for user in users) + 1
        
        new_user = {
            'id': str(user_id),  # Convert to string for consistency
            'name': name,
            'display_name': display_name,
            'creation_time': datetime.now().isoformat()
        }
        users.append(new_user)
        self._save_users(users)
        return json.dumps({'id': str(user_id)})

    def list_users(self) -> str:
        users = self._load_users()
        return json.dumps([{
            'id': user['id'],
            'name': user['name'],
            'display_name': user['display_name'],
            'creation_time': user['creation_time']
        } for user in users])

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get('id')
        if not user_id:
            raise ValueError("User ID is required")

        users = self._load_users()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            raise ValueError("User not found")

        return json.dumps({
            'name': user['name'],
            'description': f"User {user['display_name']}",
            'creation_time': user['creation_time']
        })

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get('id')
        user_data = data.get('user', {})

        if not user_id or not user_data:
            raise ValueError("User ID and user data are required")

        users = self._load_users()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            raise ValueError("User not found")

        if 'name' in user_data:
            raise ValueError("User name cannot be updated")

        if 'display_name' in user_data:
            if len(user_data['display_name']) > 128:
                raise ValueError("Display name can be max 128 characters")
            user['display_name'] = user_data['display_name']

        self._save_users(users)
        return json.dumps({'status': 'success'})

    def get_user_teams(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get('id')
        if not user_id:
            raise ValueError("User ID is required")

        # This will be implemented when we have team data
        return json.dumps([])

    def delete_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get('id')
        if not user_id:
            raise ValueError("User ID is required")

        users = self._load_users()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            raise ValueError("User not found")

        # Remove user from teams
        team_instance = Team()
        teams = team_instance._load_teams()
        for team in teams:
            if user_id in team['users']:
                team['users'].remove(user_id)
        team_instance._save_teams(teams)

        # Remove user
        users = [u for u in users if u['id'] != user_id]
        self._save_users(users)
        return json.dumps({'status': 'success'})

class Team(TeamBase):
    def __init__(self):
        self.db_file = os.path.join('db', 'teams.json')
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        os.makedirs('db', exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def _load_teams(self) -> List[Dict]:
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _save_teams(self, teams: List[Dict]):
        with open(self.db_file, 'w') as f:
            json.dump(teams, f, indent=2)

    def create_team(self, request: str) -> str:
        data = json.loads(request)
        name = data.get('name', '')
        description = data.get('description', '')
        admin = data.get('admin', '')

        if not all([name, description, admin]):
            raise ValueError("Name, description, and admin are required")

        if len(name) > 64:
            raise ValueError("Name can be max 64 characters")
        if len(description) > 128:
            raise ValueError("Description can be max 128 characters")

        teams = self._load_teams()
        if any(team['name'] == name for team in teams):
            raise ValueError("Team name must be unique")

        # Generate sequential ID starting from 101
        team_id = 101 if not teams else max(int(team['id']) for team in teams) + 1
        
        new_team = {
            'id': str(team_id),  # Convert to string for consistency
            'name': name,
            'description': description,
            'admin': admin,
            'creation_time': datetime.now().isoformat(),
            'users': []
        }
        teams.append(new_team)
        self._save_teams(teams)
        return json.dumps({'id': str(team_id)})

    def list_teams(self) -> str:
        teams = self._load_teams()
        return json.dumps([{
            'id': team['id'],
            'name': team['name'],
            'description': team['description'],
            'creation_time': team['creation_time'],
            'admin': team['admin']
        } for team in teams])

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        if not team_id:
            raise ValueError("Team ID is required")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        return json.dumps({
            'id': team['id'],
            'name': team['name'],
            'description': team['description'],
            'creation_time': team['creation_time'],
            'admin': team['admin']
        })

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        team_data = data.get('team', {})

        if not team_id or not team_data:
            raise ValueError("Team ID and team data are required")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        if 'name' in team_data:
            if len(team_data['name']) > 64:
                raise ValueError("Name can be max 64 characters")
            if any(t['name'] == team_data['name'] for t in teams if t['id'] != team_id):
                raise ValueError("Team name must be unique")
            team['name'] = team_data['name']

        if 'description' in team_data:
            if len(team_data['description']) > 128:
                raise ValueError("Description can be max 128 characters")
            team['description'] = team_data['description']

        if 'admin' in team_data:
            team['admin'] = team_data['admin']

        self._save_teams(teams)
        return json.dumps({'status': 'success'})

    def add_users_to_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        users = data.get('users', [])

        if not team_id or not users:
            raise ValueError("Team ID and users are required")

        if len(users) > 50:
            raise ValueError("Cannot add more than 50 users at once")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        team['users'].extend([u for u in users if u not in team['users']])
        self._save_teams(teams)
        return json.dumps({'status': 'success'})

    def remove_users_from_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        users = data.get('users', [])

        if not team_id or not users:
            raise ValueError("Team ID and users are required")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        team['users'] = [u for u in team['users'] if u not in users]
        self._save_teams(teams)
        return json.dumps({'status': 'success'})

    def list_team_users(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        if not team_id:
            raise ValueError("Team ID is required")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        # Get user details for each team member
        user_instance = User()
        users = user_instance._load_users()
        team_users = []
        
        for user_id in team['users']:
            user = next((u for u in users if u['id'] == user_id), None)
            if user:
                team_users.append({
                    'id': user['id'],
                    'name': user['name'],
                    'display_name': user['display_name']
                })

        return json.dumps(team_users)

    def delete_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        if not team_id:
            raise ValueError("Team ID is required")

        teams = self._load_teams()
        team = next((t for t in teams if t['id'] == team_id), None)
        if not team:
            raise ValueError("Team not found")

        # Check if team has any active boards
        board_instance = ProjectBoard()
        boards = board_instance._load_boards()
        active_boards = [b for b in boards if b['team_id'] == team_id and b['status'] == 'OPEN']
        if active_boards:
            raise ValueError("Cannot delete team with active boards")

        # Remove team
        teams = [t for t in teams if t['id'] != team_id]
        self._save_teams(teams)
        return json.dumps({'status': 'success'})

class ProjectBoard(ProjectBoardBase):
    def __init__(self):
        self.db_file = os.path.join('db', 'boards.json')
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        os.makedirs('db', exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def _load_boards(self) -> List[Dict]:
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _save_boards(self, boards: List[Dict]):
        with open(self.db_file, 'w') as f:
            json.dump(boards, f, indent=2)

    def create_board(self, request: str) -> str:
        data = json.loads(request)
        name = data.get('name', '')
        description = data.get('description', '')
        team_id = data.get('team_id', '')

        if not all([name, description, team_id]):
            raise ValueError("Name, description, and team_id are required")

        if len(name) > 64:
            raise ValueError("Board name can be max 64 characters")
        if len(description) > 128:
            raise ValueError("Description can be max 128 characters")

        boards = self._load_boards()
        if any(board['name'] == name and board['team_id'] == team_id for board in boards):
            raise ValueError("Board name must be unique for a team")

        # Generate sequential ID starting from 1001
        board_id = 1001 if not boards else max(
            int(board['id']) if board['id'].isdigit() else 1000 
            for board in boards
        ) + 1
        
        new_board = {
            'id': str(board_id),
            'name': name,
            'description': description,
            'team_id': team_id,
            'creation_time': datetime.now().isoformat(),
            'status': 'OPEN',
            'tasks': []
        }
        boards.append(new_board)
        self._save_boards(boards)
        return json.dumps({'id': str(board_id)})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get('id')
        if not board_id:
            raise ValueError("Board ID is required")

        boards = self._load_boards()
        board = next((b for b in boards if b['id'] == board_id), None)
        if not board:
            raise ValueError("Board not found")

        if not all(task['status'] == 'COMPLETE' for task in board['tasks']):
            raise ValueError("Cannot close board with incomplete tasks")

        board['status'] = 'CLOSED'
        board['end_time'] = datetime.now().isoformat()
        self._save_boards(boards)
        return json.dumps({'status': 'success'})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        title = data.get('title', '')
        description = data.get('description', '')
        user_id = data.get('user_id', '')
        board_id = data.get('board_id', '')

        if not all([title, description, user_id, board_id]):
            raise ValueError("Title, description, user_id, and board_id are required")

        if len(title) > 64:
            raise ValueError("Task title can be max 64 characters")
        if len(description) > 128:
            raise ValueError("Description can be max 128 characters")

        boards = self._load_boards()
        board = next((b for b in boards if b['id'] == board_id), None)
        if not board:
            raise ValueError("Board not found")

        if board['status'] != 'OPEN':
            raise ValueError("Can only add task to an OPEN board")

        if any(task['title'] == title for task in board['tasks']):
            raise ValueError("Task title must be unique for a board")

        # Generate sequential task ID starting from 2001
        all_tasks = []
        for b in boards:
            all_tasks.extend(b['tasks'])
        
        task_id = 2001 if not all_tasks else max(
            int(task['id']) if task['id'].isdigit() else 2000 
            for task in all_tasks
        ) + 1

        new_task = {
            'id': str(task_id),
            'title': title,
            'description': description,
            'user_id': user_id,
            'creation_time': datetime.now().isoformat(),
            'status': 'OPEN'
        }
        board['tasks'].append(new_task)
        self._save_boards(boards)
        return json.dumps({'id': str(task_id)})

    def update_task_status(self, request: str) -> str:
        data = json.loads(request)
        task_id = data.get('id')
        status = data.get('status')

        if not task_id or not status:
            raise ValueError("Task ID and status are required")

        if status not in ['OPEN', 'IN_PROGRESS', 'COMPLETE']:
            raise ValueError("Invalid status")

        boards = self._load_boards()
        for board in boards:
            task = next((t for t in board['tasks'] if t['id'] == task_id), None)
            if task:
                task['status'] = status
                self._save_boards(boards)
                return json.dumps({'status': 'success'})

        raise ValueError("Task not found")

    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get('id')
        if not team_id:
            raise ValueError("Team ID is required")

        boards = self._load_boards()
        team_boards = [b for b in boards if b['team_id'] == team_id]
        
        # Get user details for task assignments
        user_manager = User()
        users = {u['id']: u['display_name'] for u in user_manager._load_users()}

        result_boards = []
        for board in team_boards:
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
        
        return json.dumps(result_boards)

    def export_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get('id')
        if not board_id:
            raise ValueError("Board ID is required")

        boards = self._load_boards()
        board = next((b for b in boards if b['id'] == board_id), None)
        if not board:
            raise ValueError("Board not found")

        # Create output directory if it doesn't exist
        os.makedirs('out', exist_ok=True)

        # Create a file name based on board name and timestamp
        file_name = f"board_{board_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join('out', file_name)

        with open(file_path, 'w') as f:
            f.write(f"Board: {board['name']}\n")
            f.write(f"Description: {board['description']}\n")
            f.write(f"Status: {board['status']}\n")
            f.write(f"Created: {board['creation_time']}\n")
            if board.get('end_time'):
                f.write(f"Completed: {board['end_time']}\n")
            f.write("\nTasks:\n")
            
            for task in board['tasks']:
                f.write(f"\n- {task['title']}\n")
                f.write(f"  Description: {task['description']}\n")
                f.write(f"  Status: {task['status']}\n")
                f.write(f"  Created: {task['creation_time']}\n")
                if task.get('end_time'):
                    f.write(f"  Completed: {task['end_time']}\n")

        return json.dumps({'out_file': file_name})

    def delete_board(self, request: str) -> str:
        """
        Delete a board and all its tasks.
        
        :param request: A json string with the board identifier
        {
          "id" : "<board_id>"
        }
        :return: A json string with the status
        {
          "status" : "success"
        }
        """
        data = json.loads(request)
        board_id = data.get('id')
        if not board_id:
            raise ValueError("Board ID is required")

        boards = self._load_boards()
        board = next((b for b in boards if b['id'] == board_id), None)
        if not board:
            raise ValueError("Board not found")

        # Remove the board
        boards = [b for b in boards if b['id'] != board_id]
        self._save_boards(boards)
        return json.dumps({'status': 'success'}) 