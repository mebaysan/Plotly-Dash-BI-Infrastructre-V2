[![CI for `main` branch](https://github.com/mebaysan/Plotly-Dash-BI-Infrastructre-V2/actions/workflows/main.yml/badge.svg)](https://github.com/mebaysan/Plotly-Dash-BI-Infrastructre-V2/actions/workflows/main.yml)


# Dash-User-Management

A template web app built in Plotly Dash for Python, which handles user creation, user authentication/login, user permissions (admin/non admin), and page navigation.

The template uses Dash bootstrap components with the [Dash Bootstrap Components by Faculty AI](https://dash-bootstrap-components.opensource.faculty.ai/)


# Core
The template has the following **core** views:

1. `login.py` - User login page, displayed if a user tries to access any page and is not currently logged in
2. `profile.py` - For users to update their own password
3. `user_admin.py` - A page for admin users only, with ability to create new users, view existing users, create new roles and assign roles to existing users.
4. `404.py` - Simple 404 error message to catch requests for non-existent pages





# Database

All the tables will be created with the first request of the app. However, the suggested method to run app is using Database Migration. 

The application depends on `DB_URL` environment variable. To set that variable, you have to put the variable below into the `.env` file. You can work with whatever you want database if you can create a connection SQLAlchemy. An example connection string is below.


```
DB_URL=postgresql://postgres:123456@localhost:5432/app_dev_db
```

## Database Migration

`Flask-Migrate` package is used to handle database migrations.

We can use one of the following commands to init database:
- `flask db init`
- `make db-init`


When we apply changes to database models, we have to migrate them:
- `flask db migrate -m "<MIGRATION MESSAGE>"` 

One of the commands below uses for applying the migration to the database. We have to use to apply changes on the database.
- `flask db upgrade`
- `make db-upgrade`


## Database Seed

`seed` method located in `UserModel` in `models/user.py`.To use this method, firstly you should be located in the shell with app context. Then you can execute `seed` method after importing `UserModel` class.

```
flask shell

from models.user import UserModel

UserModel.seed()

>>> SEED COMPLETED SUCCESSFULLY!
```

`admin` user will be created automatically with the `default` authorization group:
- Username: `admin`
- Password: `123.`

Also, all roles will be created and assigned to the `default` authorization group.


#  Mail Setup
Mail credentials have to be located in the `.env` file.
```

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=mail@gmail.com
MAIL_PASSWORD=password
MAIL_USE_TLS=False
MAIL_USE_SSL=True
```

# Gallery

# Login Page
![](gallery/gallery-login.png)

# Overview (Index) Page
![](gallery/gallery-overview.png)

# Sidebar
![](gallery/gallery-sidebar.png)

# Profile Page
![](gallery/gallery-profile.png)

# Admin User Management Page
![](gallery/gallery-admin-users.png)

# Admin User Management Page - User Add Form
![](gallery/gallery-admin-user-add.png)

# Admin User Management Page - User Update Form
![](gallery/gallery-admin-user-update.png)

# Admin Roles Management Page
![](gallery/gallery-admin-roles.png)

# Admin Groups Management Page
![](gallery/gallery-admin-groups.png)


# License
```
MIT License

Copyright (c) [2022] [M. Enes Baysan]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```