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
  - [3 - Model Structure of The Project](#3---model-structure-of-the-project)

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

The login view here is customised to return you the primary key and email of the logged in user, as well as the token. [Check out the `CustomAuthToken` view in the source code!](https://github.com/SheCodesAus/example_finished_drf_project/blob/main/crowdfunding/users/views.py#L66)

Important points on how this works are:
1.  ```py
        class CustomAuthToken(ObtainAuthToken):
    ```
    > We create our view by building on the `ObtainAuthToken` view class that DRF provides out-of-the-box. This means that we don't need to start from scratch. Instead we just add the custom functionality we need.

2.  ```py
            def post(self, request, *args, **kwargs):
                serializer = self.serializer_class(
                    data=request.data,
                    context={'request': request}
                )
    ```
    > Next, we use the built-in serializer that comes with the `ObtainAuthToken` view to serialize the incoming request. This turns it from JSON to a Python object that we can use in our code.
3.  ```py
                serializer.is_valid(raise_exception=True)
    ```
    > Running the `serializer.is_valid()` function checks that the user entered their password correctly. In the process, the user's details are grabbed from the database.
4.  ```py
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
    ```
    We grab the logged in user's details from the serializer. This lets us use the `Token.objects.get_or_create()` method to grab a token for them!

5.  ```py
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email
                })
    ```
    Finally, since we have the token and the user's details, we can include them in our response. Easy!

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

## 3 - Model Structure of The Project
[The Entity Relationship Diagram](#entity-relationship-diagram) lays out the entity relationships for this project, but there's one thing we can look into a little deeper here, and that's the nature of the relationships between models.

All of the relationships that are explicitly depicted in the ERD are "one-to-many" relationships. Each `User` can create multiple `Exam`s. Each `User` can receive multiple `ExamResult`s. Each `TutorProject` can receive multiple `TutorPledge`s, etc. Does that mean that there aren't any other types of relationship here?

Actually, no! There are some **implicit** relationships between these entities that it's worth considering. Ask yourself: what is the nature of the relationship between students and exams?

Each student can sit multiple exams, and each exam is sat by multiple students. That means there is a **"many-to-many"** relationship here! Our `ExamResult` table is actually a "through-table" that mediates the relationship between users and the exams they take. 

(In fact there's one more implicit many-to-many relationship in this demo - tutors have a many-to-many relationship with the projects they pledge to, mediated by the `TutorPledge` table.)

We've inserted an example of how you might use this many-to-many relationship into the demo. 