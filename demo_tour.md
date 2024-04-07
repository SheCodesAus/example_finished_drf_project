# Demo Tour
This doc exists to highlight some of the key patterns and techniques that are used in this demo app. Students and mentors are encouraged to browse through! If you're a mentor giving feedback on student projects, you might find it useful to link to some of the sections below.

## 1 - Table of Contents
- [Demo Tour](#demo-tour)
  - [1 - Table of Contents](#1---table-of-contents)
  - [2 -  How To Use The Project](#2----how-to-use-the-project)
    - [2.1 - Creating Objects](#21---creating-objects)
      - [2.1.1 - Users](#211---users)
      - [2.1.2 - Exams](#212---exams)
      - [2.1.3 - ExamResults](#213---examresults)
      - [2.1.4 - TutorProjects](#214---tutorprojects)
      - [2.1.5 - TutorPledges](#215---tutorpledges)
    - [2.2 - Other Actions](#22---other-actions)
      - [2.2.1 - Logging In](#221---logging-in)
      - [2.2.2 - GETting Data](#222---getting-data)
      - [2.2.3 - Updating Data](#223---updating-data)
      - [2.2.4 - Deleting Records](#224---deleting-records)
  - [3 - Useful Patterns](#3---useful-patterns)
    - [3.1 - Many-To-Many Relationships](#31---many-to-many-relationships)
    - [3.2 - Custom Authentication Endpoint](#32---custom-authentication-endpoint)
    - [3.3 - Complex Custom `Permission` Classes](#33---complex-custom-permission-classes)
    - [3.4 - In-View Permission Handling](#34---in-view-permission-handling)
    - [3.5 - Uniqueness Constraints](#35---uniqueness-constraints)
    - [3.6 - Deleting Records](#36---deleting-records)
    - [3.7 - Response Codes](#37---response-codes)

## 2 -  How To Use The Project
Let's take a moment to look at how the project is designed to be used so we can orientate ourselves. 

### 2.1 - Creating Objects
There are a few different ways to create objects in this project. We'll go through them all.

#### 2.1.1 - Users
Users are created by making a POST request at the `/users/` endpoint. Nothing revolutionary there.

#### 2.1.2 - Exams
The `Exam` table contains records of exams that it is possible to study for. These records are created by making a POST request at the `/exams/` endpoint. You need to be logged in to create an exam, but any logged in user can create one.

#### 2.1.3 - ExamResults
The `ExamResult` table contains records of people's scores on exams they have sat. To record someone's score on an exam, you need to be logged in as the owner of that exam. This is so that people can't create their own fake scores - only the educator who marked the exam is allowed to record the scores.

These records are created by making a POST request at the `/users/<int: pk>/` endpoint.

> [!NOTE]
> You might be wondering - why aren't we making a post at the `/exam_results/` endpoint to create exam results? 
>
> The answer is that I could have coded it that way, but I chose not to. The reason for my decision has to do with a concept called "Resource-Orientated Design". Here's the TL;DR: 
> - RESTful APIs are designed to be "resource-oriented", meaning that each endpoint represents a specific resource or collection of resources. 
> - Each primary-key defined endpoint in the `/users/<int: pk>/` collection represents a single resource: a user record. 
> - `ExamResult` records don't exist in isolation. They "belong to" the user who sat the exam. We call this idea "Resource Heirarchy". 
> 
> That means it makes sense to see exam results as **part of** a `User` record. So I chose to set my API up so that `ExamResult` records are created by making a POST to the user details endpoint!
>
> **Note carefully: this is a convention.** There's no hard-and-fast rule that says you MUST structure your APIs this way. It would have been perfectly reasonable to built an `/exam_results/` endpoint, and create exam result records by POSTing to it. The important rule is that you should always clearly document your endpoints in your API spec, so that other people who use your API can find the endpoints they need.

#### 2.1.4 - TutorProjects
The `TutorProject` table contains records of study classes that need people to tutor them. These records are created by making a POST request at the `/exams/` endpoint. 

Once again, each `TutorProject` *belongs* to a specific exam, so we create them by posting to the endpoint for that individual exam! [See the note above for a detailed justification of this.](#213---examresults)

You need to be logged in as the owner of an `Exam` to create a `TutorProject` for it.

#### 2.1.5 - TutorPledges
The `TutorPledge` table contains records of pledges that tutors have made to TutorProjects. Any logged in user can make a pledge, but:
- the `TutorProject` they are pledging to must be "open", and
- they need to have an `ExamResult` associated with their account that proves they passed the exam they are pledging to tutor for (educators set the tutor grade requirement when they create the `TutorProject`)

### 2.2 - Other Actions
#### 2.2.1 - Logging In
You log in as usual at the `/api-token-auth/` endpoint. 

#### 2.2.2 - GETting Data
The following endpoints get you lists of data:
- `/users/`: The list of all users.
- `/exams/`: The list of all exams.
- `/tutor_projects/`: The list of all tutoring projects
- `/tutor_pledges/`: The list of all tutoring pledges 

The following endpoints get you the details of a specific resource:
- `/users/<int: pk>`
- `/tutor_projects/<int: pk>/`

Anyone can make a GET request at any of these endpoints!

> [!NOTE]
> Wondering why don't we have detail endpoints for the other three resources? 
>
> It's because this is an MVP! We definitely could add those endpoints in down the track, but right now, we are keeping it simple. The front-end we create based on this API will just have to get by without those extra resources.

#### 2.2.3 - Updating Data
There's only one endpoint that lets you update the details of a specific resource. You can make a PUT request at the `/tutor_projects/<int: pk>/` endpoint to update the details of a tutoring project. (As long as you are the person who created the project in the first place.)

> [!NOTE]
> Wondering about the justification for this? Here's my logic:
> 
> It makes sense that an educator might find that the requirements of a `TutorProject` have changed. Maybe more students join the class and they need more tutors, etc. So updating these objects is probably necessary. On the other hand... 
> - Updating user accounts would be nice, but the basic functionality of the site doesn't require it. This is probably the first "nice-to-have" that I would build once the MVP was complete.
> - The only info we are recording about exams is their name. If the name of an exam changes, then it's really a new, different exam. So building update functionality here isn't a priority.
> - Exam results don't change after the fact, so there shouldn't be a need for them to be updated. Educators just need to be careful when entering them!
> - If users can change their pledges after they've made them, that makes it harder for educators to organise their classes. If people really need to change their pledges, then they should delete the pledge and make a new one.

#### 2.2.4 - Deleting Records
There's only one endpoint that will let you delete a record. You can make a DELETE request at the 
`/tutor_pledges/<int: pk>/` endpoint to withdraw your pledge to be a tutor (as long as you're the one who created the pledge to begin with).

> [!NOTE]
> The justifications here are similar to the above. 
> - Tutor projects should be edited to set `is_open` to `False`, rather than being deleted.
> - Users should just stop using their accounts, rather than deleting them.
> - If an `Exam` isn't in use anymore, you can just stop creating TutorProjects for it.
> - Exam results don't stop existing once they're recorded.
>
> Of course, there's nothing to say more DELETE functionality can't be added down the track!

## 3 - Useful Patterns

### 3.1 - Many-To-Many Relationships
There is one many-to-many relationship [shown in our ERD](./README.md#entity-relationship-diagram) - the relationship between students and the exams they sit. This relationship is set up through the `ExamResult` table. Let's take a look at how this code works:

1. [The `ExamResult` model is defined here.](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/models.py#L22) Looks pretty normal - it has foreign key fields for both the person who sat the exam, and the exam that was sat. 
   
    > Just this is enough for an "implicit" many-to-many relationship - you could get a list of every person who sat a particular exam based on that exam's results, and you could get a list of every exam a person sat by looking at their results. Sometimes that's inconvenient though, so read on to see how it can be simplified!

2. [A `ManyToManyField` called `students` is added to the `Exam` model here.](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/models.py#L14) We specify three things:
   - The model on the other end of the relationship is the `User` model.
   - The table that this many-to-many relationship should be mediated "through" is the `ExamResult` table 
   - The field on the `User` model that lets us access this relationship should be called `studied_exams`

3. [A field called `studied_exams` is added to the `CustomUserDetailSerializer` here](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/users/serializers.py#L14). This will represent the relationship for us in our output. We use an `ExamSerializer` to represent the info in the field.

And that's it! After that, we can ignore the many-to-many relationship and let Django handle it. We create views to deal with the one-to-many relationships between `Users`/`ExamResults` and `Exams`/`ExamResults`, and Django takes care of all of the figuring out required to piece together which users have sat which exams. 

Here's what the output of our user details view looks like - you can see that the `User` data contains a list of exam results AND a list of the exams the user has sat:

![](./readme_images/studied_exams.png)

### 3.2 - Custom Authentication Endpoint

The login view here is customised to return you the primary key and email of the logged in user, as well as the token. [Check out the `CustomAuthToken` view in the source code!](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/users/views.py#L66)

Important points on how this works are:
1.  We create our view by building on the `ObtainAuthToken` view class that DRF provides out-of-the-box. This means that we don't need to start from scratch. Instead we just add the custom functionality we need.

2.  We use the built-in serializer that comes with the `ObtainAuthToken` view to serialize the incoming request. This turns it from JSON to a Python object that we can use in our code.
3.  Running the `serializer.is_valid()` function checks that the user entered their password correctly. In the process, the user's details are grabbed from the database.
4.  We grab the logged in user's details from the serializer. This lets us use the `Token.objects.get_or_create()` method to grab a token for them!

5.  Finally, since we have the token and the user's details, we can include them in our response. Easy!

### 3.3 - Complex Custom `Permission` Classes
There's one particularly complex permission class in this app - [`the ProjectDetailPerms` class](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/permissions.py#L11). This permission is applied to [the `ProjectDetail` view](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/views.py#L68). Let's step through how it works:

1. First we check to see if the request is using a "safe" method. (I.e. - is it a GET?) If the request method is safe, we return `True` - everyone is allowed to see the details of any project.

2. Next, we check to see if the request is a POST. If it's a post, that means that the user is trying to create a new `TutorPledge` on this project, so we have some rules to apply:
   - Only open projects can be pledged to. If the `project.is_open` field is set to `False`, we raise [a `PermissionDenied` exception](https://docs.djangoproject.com/en/5.0/ref/exceptions/#permissiondenied) - this automatically rejects the request with a 403 code.  
   - Only people who have a sufficiently high exam result can tutor for that exam. We filter the list of all exam results to get the ones that record this user's performance on this project's exam. We use [the `any()` function](https://docs.python.org/3/library/functions.html#any) to make sure that the user has at least one result that meets the `required_grade` for this project. If not, we raise another `PermissionDenied` exception. 
   - If we made it this far without raising an exception, then the user is allowed to pledge to the project, so we return `True`

3. Finally, we handle the cases where the request method is not "safe", and is not POST. I.e., PUT, PATCH, and DELETE. For these cases, we just check that the user making the request is the same person who created the project. If they're the creator, we return `True`. If not, we return `False`. 

Notice that almost all of the logic here is normal Python syntax! The `has_object_permission()` function will give you the request, the view, and the object being operated on, and you just write your own logic to decide whether or not the operation is allowed. We used three pieces of "Django Magic" in there:
- `permissions.SAFE_METHODS` let us check for requests that didn't change the database. (But we could have just explicitly checked that the method wasn't PUT/PATCH/POST/DELETE.)
- the `PermissionDenied` exception let us automatically return a 403 error with special error messages without adding any code to the view. (But we could have just returned `False` if we didn't care about special error messages.)
- `ExamResult.objects.filter()` let us get the specific rows we needed from the database. 

### 3.4 - In-View Permission Handling
Sometimes you have some restriction you just want to apply in one specific place. There's no point writing a `Permission` class for it, because it's a one-off. In those cases it's fine to write the permission logic directly into your view.

[Here's an example of this technique.](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/users/views.py#L58)

We don't want people to be able to record exam results if they're not the person who created the exam. So before we save the `ExamResult` object, we check: did this user create this exam?

If they didn't, we raise [a `PermissionDenied` exception](https://docs.djangoproject.com/en/5.0/ref/exceptions/#permissiondenied). Otherwise, we save the record as normal. Simple!

### 3.5 - Uniqueness Constraints
Quite often, you don't want users to be able to create duplicate records. In this project, we wanted every exam to have a unique name.

Enforcing this is easy - you just add `unique=True` to the field on the model. [Here's an example of this in action](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/models.py#L7).

When someone tries to create an exam with a name that is already taken, they automatically get a 400 error with a helpful message.

### 3.6 - Deleting Records
This is scary simple - [here's an example](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/views.py#L144). Note that because we're not returning any info, we can use the 204 response code - "NO CONTENT".

### 3.7 - Response Codes
It can often seem like there are wayyyyy to many response codes, and you'll never be able to make sure that your endpoints always return the correct one. In fact, Django has a few helpful tools to make this easy. Here's how I make sure my response codes are correct:

- If you don't specify a code in your `Response()` object, Django will always insert a 200_OK code. That means you never need to specify a response for successful GET, or PATCH requests!
- Every successful POST or PUT request should give a 201_CREATED code.
- Every successful DELETE request can give a 204_NO_CONTENT code.
- Every view that needs to retrieve a specific object should have a `get_object()` method like the one we demonstrated in class. [If you use this pattern](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/projects/views.py#L36), you'll always return a 404_NOT_FOUND when you're supposed to. 
- Any time you write code to check permissions, raise [a `PermissionDenied` exception](https://docs.djangoproject.com/en/5.0/ref/exceptions/#permissiondenied) if the permission is denied. Django will ensure that this results in a 403 code without you having to do anything about it. See section [3.4 - In-View Permission Handling](#34---in-view-permission-handling) above for an example of this in action.

That's it! These rules should cover pretty much every single situation you need to code for. Once you start running into weird edge cases, you'll have enough coding experience to figure them out.