## Restaurant menu voting app

This backend api is designed to provide employees with ability to vote for their menu. Supported features include:
registration of new users, registration of new restaurants(by user with admin rights), adding new menus(for users, who are specified
as restaurant owners), checking current day menus and voting results and voting(one vote for user per day)

### Technologies:

<div style="display:flex; align-items: center; gap:10px">
     Python
</div>
<div style="display:flex; align-items: center; gap:10px">
     Django
</div>
<div style="display:flex; align-items: center; gap:10px">
     Django Rest Framework
</div>
<div style="display:flex; align-items: center; gap:10px">
     simpleJWT
</div>
<div style="display:flex; align-items: center; gap:10px">
     PyTests
</div>
<div style="display:flex; align-items: center; gap:10px">
     PostgreSQL
</div>
<div style="display:flex; align-items: center; gap:10px">
     Git
</div>
<div style="display:flex; align-items: center; gap:10px">
    Postman
</div>

### Installation:

 ```bash
  git clone https://github.com/rraatt/FoodVoteApp.git
```

Create a .env.dev file and add the following variables:

 ```bash
  DEBUG=1
  SECRET_KEY=<Your key>
  DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
  SQL_ENGINE=django.db.backends.postgresql
  SQL_DATABASE=hello_django_dev
  SQL_USER=user
  SQL_PASSWORD=password
  SQL_HOST=db
  SQL_PORT=5432
```

Create and activate a virtual environment:

 ```bash
  docker-compose up -d --build
```

Apply migrations

 ```bash
  docker-compose exec webapp python ./src/manage.py migrate         
```

Register user with admin rights

 ```bash
  docker-compose exec webapp python ./src/manage.py createsuperuser     
  ```   
### Usage:

Access at localhost:

 http://localhost:8000/
