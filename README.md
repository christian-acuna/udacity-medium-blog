Medium Blog
-----------

This is a multi-user blog project written in Python 2.7 using Google App Engine

You can view it live here: [medium-blog.appspot.com/blog](https://medium-blog.appspot.com/blog)

### Requirements for local deployment ###

* [Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
* Python 2.7

---

### Quickstart

1. Clone or download repo
* Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
* cd into file directory
* run `dev_appserver.py .` to start server
* visit [http://localhost:8080/](http://localhost:8080/) to open app.

#### Deploy app
1. run `gcloud app deploy` in the root directory where the app.yaml file is located
* run `gcloud app browse` to view project in the browser

---

### About this app

This app allows users to create an account to create/edit/delete posts, like/unlike other users' posts, and create/edit/delete comments on a post.
All comments are deleted when a user deletes their own post. Semantic-UI was used for the layout and CSS to create a simple but intuitive user interface. The project is built using the webapp2 Framework hosted on Google's App Engine with Python 2.7. It leverages Google's NoSQL Schemaless Cloud Datastore to manage posts, comments, and users.

In order to create a more responsive and dynamic user experience, AJAK is used to handle the liking/unliking of posts as well as creating, editing, and deleting comments.
