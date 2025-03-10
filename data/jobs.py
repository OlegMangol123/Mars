import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"
    users = orm.relationship("user")
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
