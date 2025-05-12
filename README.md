# Project Planner - Django Assignment

A Django-based project management application that helps teams organize and track their work efficiently.

## Features

- User Management System
- Team Management
- Project Board with Task Tracking
- RESTful API Support
- Interactive Web Interface

## Tech Stack

- Python 3.x
- Django 5.0.2
- SQLite Database
- HTML/CSS/JavaScript
- Bootstrap (for UI)

## Project Structure

```
project_planner/
├── api/            # API endpoints
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
├── db/            # Database related files
└── SCREENSHOTS/   # Project screenshots
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd Django-Assignment
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Key Components

- `user_base.py`: User management functionality
- `team_base.py`: Team management system
- `project_board_base.py`: Project board and task management
- `concrete_implementation.py`: Main implementation logic

## API Endpoints

The application provides RESTful API endpoints for:
- User operations
- Team management
- Project board operations
- Task management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Key Points

- **Modular Architecture**: Implemented using abstract base classes for clean separation of concerns
- **Data Persistence**: Uses SQLite database for reliable data storage
- **RESTful API Design**: Clean and intuitive API endpoints for all operations
- **Input Validation**: Comprehensive validation for all API inputs
- **Error Handling**: Proper exception handling for edge cases
- **Scalable Design**: Easy to extend with new features
- **Clean Code**: Well-documented and maintainable codebase

## Implementation Ideas

### 1. User Management
- Implemented user registration and authentication
- User roles and permissions system
- Profile management with validation
- Secure password handling

### 2. Team Management
- Team creation and management
- Member assignment and role management
- Team hierarchy support
- Team activity tracking

### 3. Project Board System
- Kanban-style board implementation
- Task creation and assignment
- Status tracking and updates
- Priority management
- Due date handling

### 4. Technical Implementation
- Used Django's built-in ORM for database operations
- Implemented custom serializers for JSON handling
- Created reusable components for common operations
- Used Django REST framework for API endpoints
- Implemented proper validation and error handling

### 5. Design Decisions
- Chose SQLite for simplicity and portability
- Used abstract base classes for better code organization
- Implemented proper separation of concerns
- Focused on maintainable and scalable code structure

## UI Screenshots

The application features a modern and intuitive user interface. Screenshots of various features are available in the `SCREENSHOTS` directory:

- Home Page
- User Management
  - View Users
  - Add/Create User
  - Delete User
- Team Management
  - View Teams
  - Add/Create Team
  - Delete Team
  - Add Members to Team
  - Remove Team Members
- Project Board
  - View Boards
  - Add/Create Board
  - Add Tasks to Board
  - Task Tracking Status

These screenshots demonstrate the complete workflow and user experience of the application.