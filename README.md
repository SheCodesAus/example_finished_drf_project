# Crowdfunding Back End

## Table of Contents
- [Crowdfunding Back End](#crowdfunding-back-end)
  - [Table of Contents](#table-of-contents)
  - [Context](#context)
    - [Note To Students](#note-to-students)
  - [App Name: "Examplify"](#app-name-examplify)
  - [Entity Relationship Diagram](#entity-relationship-diagram)
  - [API Spec](#api-spec)
  - [Testing](#testing)


## Context
This is an example completed back-end for the She Codes Plus course content. It is intended for use in project feedback, to allow mentors to demonstrate techniques and code patterns to students, without needing to write a new app every time. 

It is NOT intended to be shared with students before their DRF projects are submitted, since it includes content they are expected to synthesise themselves.

The deployed back-end can be found here: https://example-finished-drf-project.fly.dev/

[A "tour" of some of the key concepts and patterns used in this project can be found here](./demo_tour.md)

### Note To Students
This is a relatively complex app. 

The aim here is to provide an example for most/all of the patterns and use-cases that mentors might want to demonstrate to students of the DRF module, and that means we needed to pick a slightly ambitious design. 

If I saw this kind of work from a student, I would surmise that one or more of the following was true:
- They had previous programming experience
- They had a LOT of spare time to throw into the project
- They had busted an absolute gut and were rightly proud of their effort

That means that it's perfectly fine and normal if your app is simpler or less developed than this! Remember, these projects are learning activities, not assessment activities. You're not supposed to go **IN** knowing how to ace the project; you're supposed to come **OUT** with a better understanding and an artifact that illustrates your coding journey.

Feel free to use this code as an inspiration to expand on your project after you have submitted it. And if you see something here that you'd like help interpreting or applying, feel free to reach out on slack to set up a 1-1 with a mentor.

## App Name: "Examplify"
Examplify is a crowdfunding app that allows educators to connect students in their classes with tutors who have succeeded in the class previously. 

Educators advertise upcoming exams (i.e., projects) that they need tutors for. Ex-students can pledge their time to help current students study, as long as they achieved a high enough grade on that same exam in a previous class. Educators can specify the grade they require their tutors to have achieved on an exam in order to quality to tutor for it.

## Entity Relationship Diagram
![](./readme_images/ERD.drawio.png)

## API Spec
> Scroll sideways to see the whole table!

| URL                          | HTTP Method | Purpose                                                                                                                                                                                          | Request Body                                                                                                                                                                         | Success Response Code | Authentication/Authorisation                                                                                                                                        | Complete |
| ---------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `/`                          | GET         | Returns `hello world` to prevent the root URI from returning a 404. This is just a cosmetic feature so that it's instantly clear that the demo is working when it's opened in front of students. | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/api-token-auth/`           | POST        | Obtain a JWT to use as authentication at other endpoints, as well as the details of the currently-logged-in user.                                                                                | `{`<br>`"username": ...,`<br>`"password": ...`<br>`}`                                                                                                                                | 200                   | Supply the correct username/password combo.                                                                                                                         | ✅       |
| `/users/`                    | GET         | Query the list of all users.                                                                                                                                                                     | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/users/`                    | POST        | Create a new user account.                                                                                                                                                                       | `{`<br>`"username": ...,`<br>`"email": ...,`<br>`"password: ...`<br>`}`                                                                                                              | 201                   | None                                                                                                                                                                | ✅       |
| `/users/<int: pk>/`          | GET         | Retrieve the details of a specific user.                                                                                                                                                         | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/users/<int: pk>/`          | POST        | Record a specific user's result on an exam.                                                                                                                                                      | `{`<br>`"exam_id": ...`<br>`"score": ...`<br>`}`                                                                                                                                     | 201                   | Bearer token (prefix: `"Token "`) <br>Must be the creator of the exam.                                                                                              | ✅       |
| `/exams/`                    | GET         | Get the list of all exams it is possible to sit or study for.                                                                                                                                    | N/A                                                                                                                                                                                  | 200                   | N/A                                                                                                                                                                 | ✅       |
| `/exams/`                    | POST        | Create a new exam.                                                                                                                                                                               | `{`<br>`"name": ...`<br>`}`                                                                                                                                                          | 201                   | Bearer token (prefix: `"Token "`) <br>Must select a unique name for the new exam.                                                                                                    | ✅       |
| `/exams/<int: pk>/`          | POST        | Create a new project                                                                                                                                                                             | `{`<br>`"name": ...,`<br>`"tutor_for": ...` <br>`"description": ...,`<br>`"image": ...,`<br>`"required_grade": ...,`<br>`"required_tutoring_hours": ...,`<br>`"is_open": ...`<br>`}` | 201                   | Bearer token (prefix: `"Token "`) <br>Must be the creator of the associated exam.                                                                                   | ✅       |
| `/tutor_projects/`           | GET         | Query the list of all projects                                                                                                                                                                   | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/tutor_projects/<int: pk>/` | GET         | Retrieve the details of a specific project                                                                                                                                                       | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/tutor_projects/<int: pk>/` | PUT         | Update the details of a specific project                                                                                                                                                         | Fields to be updated                                                                                                                                                                 | 201                   | Bearer token (prefix: `"Token "`. Must be the creator of the project.)                                                                                              | ✅       |
| `/tutor_projects/<int: pk>/` | POST        | Create a new pledge to a specific project.                                                                                                                                                       | `{`<br>`"hours_pledged": ...,`<br>`"comment": ...,`<br>`}`                                                                                                                           | 201                   | Bearer token (prefix: `"Token "`) <br>Must have an ExamResult that matches the exam and required_grade for this TutorProject. Also, the tutor_project must be open. | ✅       |
| `/tutor_pledges/`            | GET         | Query the list of all pledges.                                                                                                                                                                   | N/A                                                                                                                                                                                  | 200                   | None                                                                                                                                                                | ✅       |
| `/tutor_pledges/<int: pk>/`  | DELETE      | Delete a specific pledge.                                                                                                                                                                        | N/A                                                                                                                                                                                  | 204                   | Bearer token (prefix: `"Token "`) <br>Must either be the creator of the pledge, or the creator of the TutorProject                                                  | ✅       |

> Notice how not every model in the ERD has an endpoint? That's not because we're showcasing perfect design - it's because we're showcasing a ruthlessly sparse MVP! 
> 
> Perhaps a later iteration of this app would have a full set of CRUD endpoints for every model, but the goal of this module was to move fast and break stuff :) 

## Testing
The following tests take each row in the API spec table, and apply one test to each requirement that is set out there. This is important to do! I found a few errors that I had made while performing these tests. 

I used manual testing here. That means I just went through and created a test in Insomnia for to check that the app fulfilled each stipulation in the API spec. An alternative to this is automated testing - writing code that checks each test case for you, so you don't need to click around in Insomnia every time you make a change to the app. The Django/DRF docs have some information on how to perform automated testing, and that would be an impressive way to build on this project to further demonstrate your skills!

- [Automated Testing in Django](https://docs.djangoproject.com/en/5.0/topics/testing/overview/)
- [Automated Testing in DRF](https://www.django-rest-framework.org/api-guide/testing/)

> Scroll sideways to see the whole table!

| Endpoint                     | Action                                                            | JSON                                                                                                                                                                                                                          | Expected Result                                                                          | Expected Code | Success |
| ---------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------- | ------- |
| `/users/`                    | GET details of current users                                      | N/A                                                                                                                                                                                                                           | A list of current users.                                                                 | 200           | ✅      |
| `/users/`                    | POST a new user with correct details                              | `{"username": "testuser", "email": "test@user.com", "password": <PASSWORD HERE>}`                                                                                                                                             | A JSON user object.                                                                      | 201           | ✅      |
| `/users/`                    | POST a new user with INCORRECT details                            | `{}`                                                                                                                                                                                                                          | A JSON errors object                                                                     | 400           | ✅      |
| `/api-token-auth/`           | POST login with a correct email/password combo                    | `{"username": "testuser","password": <PASSWORD HERE>}`                                                                                                                                                                        | The user details including email and primary key                                         | 200           | ✅      |
| `/api-token-auth/`           | POST login with a incorrect email/password combo                  | `{ "username": "testuser", "password": "wrongpass"}`                                                                                                                                                                          | Failure to log in message                                                                | 400           | ✅      |
| `/users/<int: pk>/`          | GET the details of a specific user                                | N/A                                                                                                                                                                                                                           | Details of the user inclduing all owned exams, exam results, owned projects, and pledges | 200           | ✅      |
| `/users/<int: pk>/`          | GET the details of a user that does not exist                     | N/A                                                                                                                                                                                                                           | Not Found                                                                                | 404           | ✅      |
| `/exams/`                    | POST a correct new exam with authentication token.                | `{"name": "newexam"}`                                                                                                                                                                                                         | Details of the newly created exam.                                                       | 201           | ✅      |
| `/exams/`                    | POST a correct new exam while not authenticated                   | `{"name": "unauthenticated exam"}`                                                                                                                                                                                            | "Unauthorised" message                                                                   | 401           | ✅      |
| `/exams/`                    | POST an incorrect exam while authenticated                        | `{}`                                                                                                                                                                                                                          | Description of field errors.                                                             | 400           | ✅      |
| `/exams/`                    | POST exam with duplicate name while authenticated                 | `{"name": "newexam"}`                                                                                                                                                                                                         | Duplicate name message                                                                   | 400           | ✅      |
| `/users/<int: pk>/`          | POST a correct new exam result while authenticated                | `{"exam": 2, "score": 1}`                                                                                                                                                                                                     | Details of new exam result                                                               | 200           | ✅      |
| `/users/<int: pk>/`          | POST correct new exam result for non-existent user                | `{"exam": 2, "score": 1}`                                                                                                                                                                                                     | Not found                                                                                | 404           | ✅      |
| `/users/<int: pk>/`          | POST correct new exam result for non-existent exam                | `{"exam": 99, "score": 1}`                                                                                                                                                                                                    | Invalid pk                                                                               | 400           | ✅      |
| `/users/<int: pk>/`          | POST correct new exam result while NOT authenticated              | `{"exam": 2, "score": 1}`                                                                                                                                                                                                     | Unauthorised                                                                             | 401           | ✅      |
| `/users/<int: pk>/`          | POST correct new exam result for a different educator's exam      | `{"exam": 1, "score": 1}`                                                                                                                                                                                                     | Forbidden                                                                                | 403           | ✅      |
| `/users/<int: pk>/`          | POST malformed exam result                                        | `{}`                                                                                                                                                                                                                          | Field errors                                                                             | 400           | ✅      |
| `/exams/<int: pk>/`          | POST new project                                                  | `{"name": "newproject", "description": "a new project", "image": "https://upload.wikimedia.org/wikipedia/commons/4/48/Silly_Dog_%282277051513%29.jpg", "required_grade": 90, "required_tutoring_hours": 10, "is_open": true}` | Details of new project                                                                   | 201           | ✅      |
| `/exams/<int: pk>/`          | POST new project NOT authenticated                                | `{"name": "newproject", "description": "a new project", "image": "https://upload.wikimedia.org/wikipedia/commons/4/48/Silly_Dog_%282277051513%29.jpg", "required_grade": 90, "required_tutoring_hours": 10, "is_open": true}` | Unauthorised                                                                             | 401           | ✅      |
| `/exams/<int: pk>/`          | POST new project to non-existent exam                             | `{"name": "newproject", "description": "a new project", "image": "https://upload.wikimedia.org/wikipedia/commons/4/48/Silly_Dog_%282277051513%29.jpg", "required_grade": 90, "required_tutoring_hours": 10, "is_open": true}` | Not found                                                                                | 404           | ✅      |
| `/exams/<int: pk>/`          | POST new project to a different educator's exam                   | `{"name": "newproject", "description": "a new project", "image": "https://upload.wikimedia.org/wikipedia/commons/4/48/Silly_Dog_%282277051513%29.jpg", "required_grade": 90, "required_tutoring_hours": 10, "is_open": true}` | Forbidden                                                                                | 403           | ✅      |
| `/exams/<int: pk>/`          | POST a malformed new project                                      | {}                                                                                                                                                                                                                            | Field errors                                                                             | 400           | ✅      |
| `/tutor_projects/`           | GET list of projects                                              | N/A                                                                                                                                                                                                                           | List of projects                                                                         | 200           | ✅      |
| `/tutor_projects/<int: pk>/` | GET details of specific project                                   | N/A                                                                                                                                                                                                                           | Project details                                                                          | 200           | ✅      |
| `/tutor_projects/<int: pk>/` | GET details of project that does not exist                        | N/A                                                                                                                                                                                                                           | Not Found                                                                                | 404           | ✅      |
| `/tutor_projects/<int: pk>/` | PUT updated details of a project                                  | `{"name": "updated name"}`                                                                                                                                                                                                    | Updated project details                                                                  | 201           | ✅      |
| `/tutor_projects/<int: pk>/` | PUT updated details of project while NOT authenticated            | `{"name": "updated name"}`                                                                                                                                                                                                    | Unauthorised                                                                             | 401           | ✅      |
| `/tutor_projects/<int: pk>/` | PUT updated details of another educator's project                 | `{"name": "updated name"}`                                                                                                                                                                                                    | Forbidden                                                                                | 403           | ✅      |
| `/tutor_projects/<int: pk>/` | PUT updated details of project that does not exist                | `{"name": "updated name"}`                                                                                                                                                                                                    | Not found                                                                                | 404           | ✅      |
| `/tutor_projects/<int: pk>/` | PUT malformed project details                                     | `{"required_grade": "not a number"}`                                                                                                                                                                                          | Field errors                                                                             | 400           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a pledge to a specific project                               | `{"hours_pledged": 1, "comment": "a comment"}`                                                                                                                                                                                | Details of new pledge                                                                    | 200           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a pledge while not authenticated                             | `{"hours_pledged": 1, "comment": "a comment"}`                                                                                                                                                                                | Unauthorised                                                                             | 401           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a pledge to a project that does not exist                    | `{"hours_pledged": 1, "comment": "a comment"}`                                                                                                                                                                                | Not found                                                                                | 404           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a malformed pledge                                           | `{}`                                                                                                                                                                                                                          | Field errors                                                                             | 400           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a pledge to a project without a sufficiently high ExamResult | `{"hours_pledged": 1, "comment": "a comment"}`                                                                                                                                                                                | Forbidden                                                                                | 403           | ✅      |
| `/tutor_projects/<int: pk>/` | POST a pledge to a closed project                                 | `{"hours_pledged": 1, "comment": "a comment"}`                                                                                                                                                                                | Forbidden                                                                                | 403           | ✅      |
| `/tutor_pledges/`            | GET list of pledges                                               | N/A                                                                                                                                                                                                                           | List of pledges                                                                          | 200           | ✅      |
| `/tutor_pledges/<int: pk>/`  | DELETE a pledge as pledger                                        | N/A                                                                                                                                                                                                                           | N/A                                                                                      | 204           | ✅      |
| `/tutor_pledges/<int: pk>/`  | DELETE a pledge as pledgee                                        | N/A                                                                                                                                                                                                                           | N/A                                                                                      | 204           | ✅      |
| `/tutor_pledges/<int: pk>/`  | DELETE pledge, NOT as pledger OR pledgee                          | N/A                                                                                                                                                                                                                           | Forbidden                                                                                | 403           | ✅      |
| `/tutor_pledges/<int: pk>/`  | DELETE non existent pledge                                        | N/A                                                                                                                                                                                                                           | Not found                                                                                | 404           | ✅      |
