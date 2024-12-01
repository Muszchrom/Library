# Gateway
### Custom headers for user authentication on backend
<b>X-role-id</b> or in python <b>HTTP_X_ROLE_ID</b> consists of two values in the following format: "user_role user_id". Real world example would be "3 1"
Note that not every request would have this kind of header on itself. This type of data can only be retrieved when user is signed in. Because of that add appropriate null handlers or inform gateway maintainers about routes requiring user_role and user_id. Possible values: `"user_role user_id" | null`.

python code example to get this header: `self.request.META.get('HTTP_X_ROLE_ID')`

Roles:
* 1 - Admin
* 2 - Employee
* 3 - User

## Routes
### /auth/user
#### PATCH
Alters current record in database. User must be logged in and token must be provided. Please provide only one field that has to be changed at the time otherwise errors might occur since only one field changes per request in set order. 

<b>@Headers</b><br>
Authorization bearer with JWT. 

<b>@Body</b><br>
Takes current password and a field that has to be changed.
```
{
    "password": "student", 
    // plus one of the following
    "newPassword": "student2"
    "username": "student"
    "email": "student@student.student"
    "phone": 123123123
}
```
<b>@Response</b></br> 
```
{
    "id": 1,
    "username": "student",
    "email": "student@student.student",
    "phone": 123123123,
    "role": 3
}
``` 
