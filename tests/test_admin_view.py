from django.test import LiveServerTestCase
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from task.models import Tag, Task
from django.urls import reverse
from rest_framework.test import APIClient
from task.views import (
    TaskRetrieveUpdateDestroyAPIView,
    TagListCreateAPIView,
    TagRetrieveUpdateDestroyAPIView,
)
from rest_framework.test import APIRequestFactory
from task.serializers import CustomTagField
from task.serializers import TaskSerializer
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User


class AdminTests(LiveServerTestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.admin_username = "lk"
        self.admin_password = "livingstone"
        self.client = APIClient()

    def tearDown(self):
        self.driver.close()

    def test_login_to_admin(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        assert self.driver.title == "Site administration | Django site admin"

    def test_admin_view_add_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_success_message = "The task “Test_Task” was added successfully."
        assert expected_success_message == success_message_text
        # self.delete_task("Test_Task")

    def test_admin_view_update_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag(tag_name="Test")
        self.create_task()
        self.update_task()
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_success_message = "The task “Test_Task_updated” was changed successfully."
        assert expected_success_message == success_message_text

    def test_admin_view_delete_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.delete_task("Test_Task")
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_success_message = "Successfully deleted 1 task."
        assert expected_success_message == success_message_text

    def test_admin_view_add_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_success_message = "The tag “Test_Tag” was added successfully."
        assert expected_success_message == success_message_text

    def test_admin_view_update_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.update_tag()
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_success_message = "The tag “Test_Tag_Updated” was changed successfully."
        assert expected_success_message == success_message_text

    def test_admin_view_delete_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.delete_tag("Test_Tag")
        success_message_element = self.driver.find_element(By.CLASS_NAME, "success")
        success_message_text = success_message_element.text
        expected_message = "Successfully deleted 1 tag."
        assert expected_message == success_message_text

    def test_tag_str_method(self):
        tag = Tag.objects.create(name="Test_Tag")
        expected_str = "Test_Tag"
        actual_str = str(tag)
        self.assertEqual(expected_str, actual_str)

    def test_task_str_method(self):
        task = Task.objects.create(title="Test_Task", description="test")
        expected_str = "Test_Task"
        actual_str = str(task)
        self.assertEqual(expected_str, actual_str)
        task.delete()

    def test_task_clean_method(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.validation_error_task()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_li_text = error_li.text
        assert error_li_text == "Task Update Failed"
        if error_li_text == "Task Update Failed":
            invalid_data = {
                "title": "Test_Task",
                "description": "description",
                "due_date": "2020-12-01",
                "tags": ["Test_Tag"],
                "status": "OPEN",
            }
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            request = factory.post(url, data=invalid_data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request)
            assert response.status_code == 400

    def test_task_save_method(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.save_task()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_li_text = success_li.text
        assert success_li_text == "Task Saved Successfully"
        factory = APIRequestFactory()
        url = reverse("tasks-list-create")
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2024-12-01",
            "tags": ["Test_Tag1", "Test_Tag2"],
            "status": "OPEN",
        }
        request = factory.post(url, data=data, format="json")
        force_authenticate(request, user=self.user)
        view = TaskRetrieveUpdateDestroyAPIView.as_view()
        response = view(request)
        assert response.status_code == 201

    def test_get_queryset(self):
        tag = Tag.objects.create(name="Test_Tag")
        custom_tag_field_serializer = CustomTagField()
        tag_queryset = custom_tag_field_serializer.get_queryset()
        self.assertIn(tag, tag_queryset)

    def test_task_update(self):
        tag = Tag.objects.create(name="Test_Tag")
        task = Task(title="Test_Task", description="Sample description")
        task.save()
        task.tags.add(tag)
        updated_data = {
            "title": "Test_Task_Updated",
            "description": "Updated description",
            "due_date": "2024-12-31",
            "status": "DONE",
            "tags": ["New_Tag"],
        }
        serializer = TaskSerializer(instance=task, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        updated_title = task.title
        assert updated_title == "Test_Task_Updated"

    def test_get_all_tasks(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.get_all_task()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "All Tasks"
        if success_text == "All Tasks":
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request)
            assert response.status_code == 200

    def test_get_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.get_task()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Task with PK"
        if success_text == "Task with PK":
            task = Task.objects.create(title="Test_Task", description="TEST")
            task_id = task.id
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task_id})
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=task_id)
            assert response.status_code == 200

    def test_get_invalid_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.get_invalid_task()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task with Invalid PK"
        if error_text == "Task with Invalid PK":
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def test_post_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.post_task()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Task Created"
        if success_text == "Task Created":
            data = {
                "title": "Test_Task",
                "description": "description",
                "due_date": "2024-12-01",
                "tags": ["Test_Tag", "Test_Tag"],
                "status": "OPEN",
            }
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            request = factory.post(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request)
            assert response.status_code == 201

    def test_post_task_illegal(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.post_task_illegal()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task Not Created"
        if error_text == "Task Not Created":
            invalid_data = {"title": "Test_Task", "description": "description", "test": "test"}
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            request = factory.post(url, data=invalid_data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request)
            assert response.status_code == 400

    def test_put_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.put_task()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Task Updated"
        self.delete_task("Test_Task_Updated")
        if success_text == "Task Updated":
            task = Task.objects.create(title="Test_Task", description="TEST")
            task_id = task.id
            data = {"title": "Test_Task_Updated"}
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task_id})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=task_id)
            assert response.status_code == 200

    def test_put_invalid_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.put_invalid_task()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task with Invalid PK"
        if error_text == "Task with Invalid PK":
            data = {"title": "Test_Task_Updated"}
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def test_put_illegal_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.put_task_illegal()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task with Illegal Items"
        self.delete_task("Test_Task")
        if error_text == "Task with Illegal Items":
            task = Task.objects.create(title="Test_Task", description="Test")
            task_id = task.id
            data = {"title": "Test_Task_Updated", "test": "test"}
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task_id})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=task_id)
            assert response.status_code == 400

    def test_put_due_date_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.put_due_date_task()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task with Illegal Due Date"
        self.delete_task("Test_Task")
        if error_text == "Task with Illegal Due Date":
            task = Task.objects.create(title="Test_Task", description="Test")
            task_id = task.id
            data = {"title": "Test_Task_Updated", "due_date": "2020-12-12"}
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task_id})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=task_id)
            assert response.status_code == 400

    def test_delete_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.delete_task_valid()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Task Deleted"
        if success_text == "Task Deleted":
            task = Task.objects.create(title="Test_Task", description="TEST")
            task_id = task.id
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task_id})
            request = factory.delete(url)
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=task_id)
            assert response.status_code == 204

    def test_delete_invalid_task(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_task()
        self.delete_invalid_task()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Task with Invalid PK"
        if error_text == "Task with Invalid PK":
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            request = factory.delete(url)
            force_authenticate(request, user=self.user)
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def test_get_tags(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.get_tags()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "All Tags"
        self.delete_tag()
        if success_text == "All Tags":
            factory = APIRequestFactory()
            url = reverse("tag-list-create")
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TagListCreateAPIView.as_view()
            response = view(request)
            assert response.status_code == 200

    def test_post_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag(tag_name="Existing Tag")
        self.post_tag()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Tag Created"
        self.delete_tag("Test_Tag")
        self.delete_tag("Existing Tag")
        if success_text == "Tag Created":
            data = {"name": "Test_Tag"}
            factory = APIRequestFactory()
            url = reverse("tag-list-create")
            request = factory.post(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TagListCreateAPIView.as_view()
            response = view(request)
            assert response.status_code == 201

    def test_post_tag_invalid(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag(tag_name="Existing Tag")
        self.post_tag_invalid()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Tag Not Created"
        self.delete_tag("Existing Tag")
        if error_text == "Tag Not Created":
            data = {"names": "Test_Tag"}
            factory = APIRequestFactory()
            url = reverse("tag-list-create")
            request = factory.post(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TagListCreateAPIView.as_view()
            response = view(request)
            assert response.status_code == 400

    def test_get_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.get_tag()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Tag with PK"
        self.delete_tag()
        if success_text == "Tag with PK":
            tag = Tag.objects.create(name="Test_Tag")
            tag_id = tag.id
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag_id})
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=tag_id)
            assert response.status_code == 200

    def test_get_invalid_tag(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.get_invalid_tag()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Tag with Invalid PK"
        self.delete_tag()
        if error_text == "Tag with Invalid PK":
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            request = factory.get(url)
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def test_put_tag_valid(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.put_tag_valid()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Tag Updated"
        self.delete_tag("Test_Tag_Updated")
        if success_text == "Tag Updated":
            tag = Tag.objects.create(name="Test_Tag")
            tag_id = tag.id
            data = {"name": "Test_Tag_Updated"}
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag_id})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=tag_id)
            assert response.status_code == 200

    def test_put_tag_invalid(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        tag_id = self.get_tag_id()
        self.put_tag_invalid()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Tag Not Updated"
        self.delete_tag("Test_Tag")
        if error_text == "Tag Not Updated":
            tag = Tag.objects.create(name="Test_Tag")
            tag_id = tag.id
            data = {"names": "Test_Tag_Updated"}
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag_id})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=tag_id)
            assert response.status_code == 400

    def test_put_tag_invalid_id(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.put_tag_invalid_id()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Tag with Invalid PK"
        self.delete_tag("Test_Tag")
        if error_text == "Tag with Invalid PK":
            data = {"name": "Test_Tag_Updated"}
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            request = factory.put(url, data=data, format="json")
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def test_delete_tag_valid(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        tag_id = self.get_tag_id("Test_Tag")
        self.delete_tag_valid()
        success_li = self.driver.find_element(By.CSS_SELECTOR, "li.success")
        success_text = success_li.text
        assert success_text == "Tag Deleted"
        if success_text == "Tag Deleted":
            tag = Tag.objects.create(name="Test_Tag")
            tag_id = tag.id
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag_id})
            request = factory.delete(url)
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=tag_id)
            assert response.status_code == 204

    def test_delete_tag_invalid(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.login_to_admin()
        self.create_tag()
        self.delete_tag_invalid()
        error_li = self.driver.find_element(By.CSS_SELECTOR, "li.error")
        error_text = error_li.text
        assert error_text == "Tag with Invalid PK"
        self.delete_tag("Test_Tag")
        if error_text == "Tag with Invalid PK":
            factory = APIRequestFactory()
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            request = factory.delete(url)
            force_authenticate(request, user=self.user)
            view = TagRetrieveUpdateDestroyAPIView.as_view()
            response = view(request, pk=10000000000000000)
            assert response.status_code == 400

    def delete_tag_invalid(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete Tag Invalid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def delete_tag_valid(self):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = '//th[contains(a, "Test_Tag")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete Tag Valid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_tag_invalid_id(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Put Tag Invalid PK"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_tag_invalid(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Update Tag Invalid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_tag_valid(self):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = '//th[contains(a, "Test_Tag")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Update Tag Valid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_tag_id(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        id_element = self.driver.find_element(By.CSS_SELECTOR, "td.field-id")
        id_value = id_element.text
        return id_value

    def get_invalid_tag(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Get Tag Invalid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_tag(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(By.XPATH, '//select[@name="action"]/option[text()="Get Tag"]')
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def post_tag_invalid(self):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Existing Tag")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Post Tag Invalid"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def post_tag(self):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Existing Tag")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Post Tag"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_tags(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{tag_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Get Tags"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def delete_invalid_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete Task Invalid"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def delete_task_valid(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete Task Valid"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_due_date_task(self):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Test_Task")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Put Task Due Date"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_task_illegal(self):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Test_Task")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Put Task Illegal"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_invalid_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Update Task Invalid"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def put_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Update Task Valid"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def post_task_illegal(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Post Task Illegal"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def post_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Post Task"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_invalid_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Get Task Invalid"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Get Task"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def get_all_task(self):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Test_Task")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        click_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Get all Tasks"]'
        )
        click_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def login_to_admin(self):
        url = self.live_server_url + "/admin/"
        print(url)
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys(self.admin_username)
        password_input.send_keys(self.admin_password)
        password_input.send_keys(Keys.RETURN)

    def create_task(
        self,
        title="Test_Task",
        description="This is a test task",
        due_date="2024-01-01",
        status="OPEN",
        tag_name="",
    ):
        url = self.live_server_url + "/admin/task/task/add/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_title")))
        title_input = self.driver.find_element(By.ID, "id_title")
        title_input.send_keys(title)
        description_input = self.driver.find_element(By.ID, "id_description")
        description_input.send_keys(description)
        due_date_input = self.driver.find_element(By.ID, "id_due_date")
        due_date_input.send_keys(due_date)
        select_status = Select(self.driver.find_element(By.ID, "id_status"))
        select_status.select_by_value(status)
        if tag_name != "":
            select_tag = Select(self.driver.find_element(By.ID, "id_tags"))
            select_tag.select_by_visible_text(tag_name)
        submit_button = self.driver.find_element(By.NAME, "_save")
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))

    def delete_task(self, task_name):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete selected tasks"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))
        )
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))

    def get_task_id(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        id_element = self.driver.find_element(By.CSS_SELECTOR, "td.field-id")
        id_value = id_element.text
        return id_value

    def get_task_title(self):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Test_Task_Updated")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        id_element = self.driver.find_element(By.CSS_SELECTOR, "th.field-title")
        id_value = id_element.text
        return id_value

    def validation_error_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Update Task"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def save_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Save Task"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def tag_get_queryset(self):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        task_checkbox_xpath = (
            '//th[contains(a, "Existing Tag")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Test Get Query Set"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def add_tag_to_task(self, task_name="Test_Task"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        task_checkbox_xpath = (
            f'//th[contains(a, "{task_name}")]/' 'preceding-sibling::td/input[@type="checkbox"]'
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, task_checkbox_xpath)))
        task_checkbox = self.driver.find_element(By.XPATH, task_checkbox_xpath)
        task_checkbox.click()
        task_checkbox = self.driver.find_element(By.NAME, "action")
        task_checkbox.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Add a tag to the task"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "messagelist")))

    def update_task(self, update_due_date="2025-12-31"):
        url = self.live_server_url + "/admin/task/task/"
        self.driver.get(url)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Test_Task"]'))
        )
        element.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "historylink")))
        title_input = self.driver.find_element(By.ID, "id_title")
        title_input.clear()
        title_input.send_keys("Test_Task_updated")
        description_input = self.driver.find_element(By.ID, "id_description")
        print(description_input.text)
        description_input.clear()
        description_input.send_keys("This is a test task updated.")
        due_date_input = self.driver.find_element(By.ID, "id_due_date")
        print(due_date_input.text)
        due_date_input.clear()
        due_date_input.send_keys(update_due_date)
        select_status = Select(self.driver.find_element(By.ID, "id_status"))
        select_status.select_by_value("DONE")
        select_tag = Select(self.driver.find_element(By.ID, "id_tags"))
        select_tag.select_by_visible_text("Test")
        submit_button = self.driver.find_element(By.NAME, "_save")
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))

    def create_tag(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/add/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_name")))
        title_input = self.driver.find_element(By.ID, "id_name")
        title_input.send_keys(tag_name)
        submit_button = self.driver.find_element(By.NAME, "_save")
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))

    def update_tag(self, tag_name="Test_Tag_Updated"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Test_Tag"]'))
        )
        element.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "historylink")))
        title_input = self.driver.find_element(By.ID, "id_name")
        title_input.clear()
        title_input.send_keys(tag_name)
        submit_button = self.driver.find_element(By.NAME, "_save")
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))

    def delete_tag(self, tag_name="Test_Tag"):
        url = self.live_server_url + "/admin/task/tag/"
        self.driver.get(url)
        tag_checkbox_xpath = f'//th[contains(a, "{tag_name}")]/preceding-sibling::td/input[@type="checkbox"]'
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, tag_checkbox_xpath)))
        tag_checkbox = self.driver.find_element(By.XPATH, tag_checkbox_xpath)
        tag_checkbox.click()
        tag_action = self.driver.find_element(By.NAME, "action")
        tag_action.click()
        delete_action = self.driver.find_element(
            By.XPATH, '//select[@name="action"]/option[text()="Delete selected tags"]'
        )
        delete_action.click()
        confirm_delete_button = self.driver.find_element(By.NAME, "index")
        confirm_delete_button.click()
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))
        )
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
