# Task Management API

## Setup Instructions

1. Install Python 3.12

2. Install Virtualenv library
   ```bash
   pip install virtualenv
   ```
3. Create Virtual env
   ```bash
   python -m venv assignmentEnv
   ```
4. Activate Virtual Env
   ```bash
   ./assignmentEnv/Scripts/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Create PostgreSQL DB named `briskcoveyAssignment`

7. Set environment variables in Config file:
   - `DATABASE_URL=postgresql://postgres:password@localhost/briskcoveyAssignment`

8. Run Seed script
   ```bash
   python seed.py
   ```
9. Run the server:
   ```bash
   python run.py
   ```

## API Endpoints

- **GenerateToken**: `/masterlogin/`
- **Users**: `/users/`
- **Projects**: `/projects/`
- **Tasks**: `/tasks/`
