import json
import pytest
from django.urls import reverse
from rest_framework import status
from django.db import connection

@pytest.fixture(autouse=True, scope="function")
def create_tasks_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)
    yield
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS tasks")

@pytest.mark.django_db
class TestTasksAPI:

    def test_create_task(self, client):
        url = reverse("task_list")
        payload = {
            "title": "Buy groceries",
            "description": "Milk, Eggs, Bread",
            "due_date": "2025-08-10"
        }
        response = client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        # assert "The Task Added Succefully" in response.json()["message"]

    def test_create_task_missing_field(self, client):
        """Negative test: missing description field"""
        url = reverse("task_list")
        payload = {
            "title": "Incomplete Task",
            "due_date": "2025-08-10"
        }
        response = client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "is required" in response.json()["error"] or "are required" in response.json()["error"]

    def test_create_task_invalid_date(self, client):
        """Negative test: invalid due_date format"""
        url = reverse("task_list")
        payload = {
            "title": "Bad Date Task",
            "description": "This should fail",
            "due_date": "invalid-date"
        }
        response = client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_417_EXPECTATION_FAILED]
        assert "due_date" in response.json()["error"].lower()

    def test_get_task_list(self, client):
        url = reverse("task_list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_get_single_task_not_found(self, client):
        url = reverse("task_detail", kwargs={"pk": 999})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Task not found" in response.json()["error"]

    def test_update_task(self, client):
        create_url = reverse("task_list")
        task = {
            "title": "Old Task",
            "description": "Old description",
            "due_date": "2025-08-11"
        }
        res = client.post(create_url, data=json.dumps(task), content_type="application/json")
        task_id = res.json().get("id", 1)

        url = reverse("task_detail", kwargs={"pk": task_id})
        payload = {"title": "Updated Task"}
        response = client.put(url, data=json.dumps(payload), content_type="application/json")
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert "Task updated successfully" in response.json()["message"]

    def test_delete_task(self, client):
        create_url = reverse("task_list")
        task = {
            "title": "To Delete",
            "description": "Delete me",
            "due_date": "2025-08-12"
        }
        res = client.post(create_url, data=json.dumps(task), content_type="application/json")
        task_id = res.json().get("id", 1)

        url = reverse("task_detail", kwargs={"pk": task_id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert "Task Deleted Successfully" in response.json()["succcess"]
