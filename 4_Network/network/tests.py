from django.test import TestCase

from .models import User, Post, UserFollowing

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        # Create Users
        self.u1 = User.objects.create_user("user1", "user1@email.com", "user1pass")
        self.u2 = User.objects.create_user("user2", "user2@email.com", "user2pass")
        self.u3 = User.objects.create_user("user3", "user3@email.com", "user3pass")

        # Create Posts
        Post.objects.create(user=self.u1, content="Post content by user 1")

        # Follow users
        UserFollowing.objects.create(follower=self.u2, followed=self.u1)
        UserFollowing.objects.create(follower=self.u2, followed=self.u3)
        UserFollowing.objects.create(follower=self.u3, followed=self.u1)

    def test_post_content(self):
        p = Post.objects.first()
        self.assertEqual(p.content, "Post content by user 1")

    def test_post_edit_content(self):
        p = Post.objects.first()
        p.content = "Edited post content by user 1"
        p.save()
        self.assertEqual(p.content, "Edited post content by user 1")

    def test_post_count_likes(self):
        p = Post.objects.first()
        p.likes.add(self.u1)
        p.likes.add(self.u2)
        p.likes.add(self.u3)
        self.assertEqual(p.likes.all().count(), 3)

    def test_valid_user_following(self):
        self.assertEqual(self.u2.following.all().count(), 2)

    def test_count_followers(self):
        self.assertEqual(self.u3.followers.all().count(), 1)

    # def test_invalid_user_following(self):
    #     f = UserFollowing.objects.create(follower=self.u1, followed=self.u1)
    #     # self.assertEqual(self.u1.followers.all().count(), 2)
    #     self.assertEqual(f.follower, f.followed)