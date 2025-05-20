from app import create_app, db
from app.models.user import User, MasterUser
from app.models.project import Project
from app.models.task import Task

app = create_app()
with app.app_context():
    db.create_all()

    u1 = User(name="TestUser1", email="testuser1@gmail.com")
    u2 = User(name="TestUser2", email="testUser2@gmail.com")
    u3 = User(name="TestUser3", email="testuser3@gmail.com")
    db.session.add_all([u1, u2, u3])

    p1 = Project(name="Project Testing", description="Project Testing Description")
    db.session.add(p1)
    db.session.flush()

    m1 = MasterUser(name="Master Admin", email="master@gmail.com")
    m1.set_password("123456")
    db.session.add(m1)
    db.session.flush()

    t1 = Task(title="testing task t1", project_id=p1.id, user_id=u1.id)
    t2 = Task(title="testing task t2", project_id=p1.id, user_id=u2.id)
    t2.dependencies.append(t1)

    t3 = Task(title="testing task t3", project_id=p1.id, user_id=u3.id)
    t4 = Task(title="testing task t4", project_id=p1.id, user_id=u1.id)
    t4.dependencies.append(t3)
    db.session.add_all([t3, t4])

    db.session.commit()
