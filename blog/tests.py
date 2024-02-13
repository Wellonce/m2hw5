import datetime

from django.test import TestCase, RequestFactory
from django.urls import reverse

from blog.models import User, Post
from .views import home_page


class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(first_name="Jahongir",
                                   last_name="Pulatov",
                                   username="jahongir",
                                   email="jahongir2@gmail.com")
        user.set_password("testpass")
        user.save()
        self.user = user
        user2 = User.objects.create(first_name="Ahrorjon",
                                    last_name="Hoshimjonov",
                                    username="ahrorjon",
                                    email="ahrorjon@gmail.com")
        user2.set_password("testpass")
        user2.save()
        self.user2 = user2
        post = Post.objects.create(title="Post1",
                                   content="Content1",
                                   author=self.user,
                                #    published=datetime.datetime.now().date().strftime("%Y-%d-%m"),
                                   is_active=True
                                   )
        self.post = post

    def test_post_detail(self):
        response = self.client.get(reverse('blog:post-detail', kwargs={"pk": self.post.id}))
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.author.first_name)
        self.assertContains(response, self.post.author.last_name)

    def test_post_inactive_detail(self):
        pass
        # self.assertNotContains()

    def test_user_profile_post_title(self):
        pass

    def test_no_post_profile(self):
        self.client.login(username=self.user2.username, password="testpass")
        response = self.client.get(reverse("blog:user-profile", kwargs={"username": self.user2.username}))
        self.assertContains(response, "No Post")

    # def test_home_post_list(self):
        
        def test_pagination(self):
            request = self.factory.get('/home/?size=2&page=1')
            response = home_page.as_view()(request)
            self.assertEqual(response.status_code, 200)
            self.assertTrue('page_obj' in response.context_data)
            self.assertTrue('num_pages' in response.context_data)
            self.assertEqual(response.context_data['page_obj'].paginator.per_page, 2)