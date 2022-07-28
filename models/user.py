from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from mail import mail
from flask_mail import Message
import os

UserAuthorizationGroup = db.Table(
    "user_group",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id")),
)


AuthorizationGroupRole = db.Table(
    "group_role",
    db.Model.metadata,
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


"""
AuthorizationGroups
- id
- name


RoleModel
- 
"""


class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, _name):
        self.name = _name

    def __repr__(self):
        return self.name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_users_count(self):
        return len(self.users)

    @classmethod
    def show_table(cls):
        roles = []

        for result in cls.query.all():
            roles.append(
                {
                    "id": result.id,
                    "rolename": result.name,
                    "usercount": result.get_users_count(),
                }
            )

        return roles


class AuthorizationGroupModel(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    roles = db.relationship(
        "RoleModel",
        secondary=AuthorizationGroupRole,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def __init__(self, _name):
        self.name = _name

    def __repr__(self):
        return self.name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    holding = db.Column(db.String, nullable=False)
    group = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True)
    # email = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    authorization_groups = db.relationship(
        "AuthorizationGroupModel",
        secondary=UserAuthorizationGroup,
        lazy="subquery",
        backref=db.backref("groups", lazy=True),
    )
    login_logs = db.relationship("LoginLog", backref="user", lazy=True)

    def __init__(self, name, position, holding, group, company, email, is_admin):
        self.name = name
        self.position = position
        self.holding = holding
        self.group = group
        self.company = company
        self.email = email
        self.is_admin = is_admin
        self.created_date = datetime.now()
        self.updated_date = datetime.now()

    def __repr__(self):
        return self.email

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def delete_from_db(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def set_password(self, _password):
        self.password = generate_password_hash(_password)

    def check_password(self, _password):
        return check_password_hash(self.password, _password)

    def is_my_role(self, role):
        # check is the role in the group roles of the user
        role = RoleModel.find_by_name(role)
        for authorization_groups in self.authorization_groups:
            if role in authorization_groups.roles:
                return True
        return False

    @classmethod
    def send_user_password(cls, user_id, password):
        user = cls.find_by_id(user_id)
        try:
            msg = Message(
                "Your account is created!",
                sender=os.environ["MAIL_USERNAME"],
                recipients=[user.email],
            )
            msg.body = f"Hey {user.name}, your account has been created successfully! Your password: {password}"
            mail.send(msg)
            return True
        except Exception as e:
            print("ERROR: ", e)
            return False

    @classmethod
    def seed(cls):
        """
            Database seeder
        """
        if not UserModel.find_by_email("admin@admin.com"):
            admin_user = UserModel(
                "Admin Osman",
                "Developer",
                "A Holding",
                "B Group",
                "C Company",
                "admin@admin.com",
                True,
            )
            admin_user.set_password("123.")
            admin_user.save_to_db()

            auth_group = AuthorizationGroupModel("default")
            auth_group.save_to_db()

            default_roles = [
                "page-overview",
                "page-projects",
                "page-project-detail",
                "page-warehouse",
                "page-hr-operations",
                "page-other-operations",
                "page-group-comparison",
                "page-region-comparison",
                "page-data",
                "access-executive-dashboard",
                "access-sap-success-factor",
                "access-portal",
            ]

            for new_role_name in default_roles:
                new_role = RoleModel(new_role_name)
                new_role.save_to_db()
                auth_group.roles.append(new_role)
                auth_group.save_to_db()

            admin_user.authorization_groups.append(auth_group)
            admin_user.save_to_db()

            auth_group2 = AuthorizationGroupModel("Authorization Group 2")
            auth_group2.save_to_db()

            auth_group3 = AuthorizationGroupModel("Authorization Group 3")
            auth_group3.save_to_db()
            print("SEED COMPLETED SUCCESSFULLY!")


class LoginLog(db.Model):
    __tablename__ = "login_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    login_datetime = db.Column(db.DateTime, nullable=False)
    login_date = db.Column(db.Date, nullable=False)
    login_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        user = UserModel.find_by_id(self.user_id)
        return f"{user.email} - {self.login_date} {self.login_time}"

    def __init__(self, user_id, login_datetime, login_date, login_time):
        self.user_id = user_id
        self.login_datetime = login_datetime
        self.login_date = login_date
        self.login_time = login_time

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
