
<h1 align="center">
   <br>
  <a><img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fgiphy.com%2Fexplore%2Fdj-crowd&psig=AOvVaw3KpAR54zDuDLfW6voArVQC&ust=1634312185746000&source=images&cd=vfe&ved=0CAkQjRxqFwoTCNjC98CdyvMCFQAAAAAdAAAAABAD" width="250"></a>
  <br>
  <br>
  The Concert search
  <br>
</h1>

<h4 align="center">The Concert search backend</h4>
Forum core with API data management

### Fast start

To clone and run this application, you'll need [Git](https://git-scm.com). 
From your command line:

```bash
# Clone this repository
$ git clone https://github.com/HryhorenkoVitalii/Core-for-forum.git


```

### API endpoints
```bash
# GET to view all users, POST to creae new.
/api/v1/user/

# GET to view users id=pk, PUT to update user, DELETE to delete user.
api/v1/user/<int:pk>

# GET to view all posts, POST to creae post.
api/v1/post/

# GET to view post id=pk, PUT to update post, DELETE to delete post.
api/v1/user/<int:pk>

# GET to view all comments, POST to creae comment.
api/v1/comment/

# GET to view comment id=pk, PUT to update comment, DELETE to delete pomment.
api/v1/comment/<int:pk>
```

## Credits

This software uses the following open source packages:

- [Django](https://www.djangoproject.com/)
- [djangorestframework](https://www.django-rest-framework.org/)
