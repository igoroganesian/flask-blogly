from models import User, Post
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # TODO: Ask if there is a way to avoid having to do this
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """ Tests the user list page includes the test user """

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_new_user_form(self):
        """ Tests the new user form page has the appropriate <H1>"""

        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Create a user", html)

    def test_new_user_redirect(self):
        """ Tests redirection to user list after new user creation """

        with self.client as c:
            resp = c.post('/users/new',
                          data={
                              'first_name': 'test2_first',
                              'last_name': 'test2_last',
                              'image_url': 'http://foo.com/'
                          })
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

            newuser = User.query.filter_by(
                first_name='test2_first'
            ).all()
            self.assertTrue(newuser)

    def test_new_user_creation(self):
        """ Tests to make sure new user is created """

        with self.client as c:
            resp = c.post('/users/new',
                          data={
                              'first_name': 'test3_first',
                              'last_name': 'test3_last',
                              'image_url': 'http://foo.com/'
                          }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test3_first", html)
            self.assertIn("test3_last", html)

    def test_userid_404(self):
        """ Tests user ID endpoints to 401 on invalid ID """

        with self.client as c:
            resp = c.get(f"/users/notreal")
            self.assertEqual(resp.status_code, 404)
            # resp = c.get(f"/users/0")
            # self.assertEqual(resp.status_code, 404)

    # Test User ID Endpoints Return 401 if Invalid ID
    # Test User Deletion Redirection and DB State
    # Test User Deletion Removes User from User List
    # Test Edit User Form Display
    # Test Edit User Redirection and DB State
    # Test Edit User Changed User Name on User List

class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id
        self.first_name = test_user.first_name
        self.last_name = test_user.last_name

        test_post1 = Post(
            title="testpost1_title",
            content="testpost1_content",
            user_id=test_user.id
        )

        db.session.add(test_post1)
        db.session.commit()

        self.post_id = test_post1.id

    def tearDown(self):

        db.session.rollback()

    def test_list_posts(self):
        """ Tests the post list on user page includes the test post """

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("testpost1_title", html)

    def test_post_details(self):
        """ Tests the post page contains test post title and content """

        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("testpost1_title", html)
            self.assertIn("testpost1_content", html)

    def test_new_post_form(self):
        """ Tests the new post form contains 'Add Post for <user>' """

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn(
                f"Add Post for {self.first_name} {self.last_name}", html)

    # technically this is testing the new post creation moreso than redirect
    def test_new_post_redirect(self):
        """ Tests redirection to user details page after new post creation """

        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new',
                          data={
                              'title': 'test_title2',
                              'content': 'test_content2',
                          }, follow_redirects=False)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.user_id}")

            newpost = Post.query.filter_by(
                title='test_title2'
            ).all()
            self.assertTrue(newpost)

    def test_new_post_creation(self):
        """ Tests to make sure new post is created """

        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={
                    'title': 'test_title2',
                    'content': 'test_content2',
                    },
                follow_redirects=True
            )

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test_title2", html)

    def test_postid_404(self):
        """ Tests user ID endpoints to 401 on invalid ID """

        with self.client as c:
            resp = c.get(f"/posts/notreal")
            self.assertEqual(resp.status_code, 404)



    # Test Edit Post Page Display
    # Test Edit Post Redirect and DB State
    # Test Edit Post Changes Post on Post Details
    # Test Post Deletion Redirect and DB State
    # Test Post Deletion Removes Post from User List
    # Test Delete User Fails if Posts Exist