from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status 
from django.db import connection
import json
from datetime import datetime
# Create your views here.



@api_view(['GET','POST'])
def tasks_ApiView(request):

# # Handling Create Task Request
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)

        try:
            title = data['title']
            description = data['description']
            due_date = data['due_date']
            
            

        except Exception as e:
             return JsonResponse(
                {"error": f"{e} is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            due_date = validate_due_date(due_date)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not title or not description or not due_date:
            return JsonResponse(
                {"error": "All fields (title, description, due_date, status) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO tasks(title,description,due_date) VALUES(%s,%s,%s) ",
                           [title,description,due_date]
                           
                           )
            cursor.close()
        return JsonResponse(data={'message':'The Task Added Succefully and Default Task Status Is Pending'}, status = status.HTTP_201_CREATED)  
      
# Handling Get all Tasks Request

    with connection.cursor() as cursor:
        cursor.execute("SELECT id ,title,description,due_date,status FROM tasks") 
        task_data = cursor.fetchall()

        task = [{'id':task[0],'title':task[1],'description':task[2],'due_date':task[3],'status':task[4]} for task in task_data]
        cursor.close()

    return JsonResponse(data=task , status = status.HTTP_200_OK , safe=False) 



@api_view(['GET' ,'PUT', 'DELETE'])
def task_detailApiView(request ,pk):

# Handling Update Detail Request

    if request.method == 'PUT':
        data = json.loads(request.body)
        
        fields = []
        values = []

        if 'due_date' in data:
            try:
                data['due_date'] = validate_due_date(data['due_date'])
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        try:

            for key, value in data.items():
                fields.append(f"{key}=%s")
                values.append(value)

            sql_query = f"UPDATE tasks SET {', '.join(fields)} WHERE id=%s"
            values.append(pk)

            with connection.cursor() as cursor:
                cursor.execute(sql_query, values)
                # connection.commit()
                cursor.close()
            return JsonResponse({"message": "Task updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Handling Delete Request
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                sql_query = "DELETE FROM tasks WHERE id=%s"
                task_to_delete = (pk , )
                cursor.execute(sql_query , task_to_delete)
                # connection.commit()
                cursor.close()
        except TypeError:
            return JsonResponse({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)  
        
        return JsonResponse(data={'succcess':'Task Deleted Successfully'} , status = status.HTTP_200_OK)    
    
# Handling Get Detail Request
    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM tasks WHERE id=%s"
        task_to_show = (pk , )
        
        
        try:
            cursor.execute(sql_query, task_to_show)
            task = cursor.fetchone()
           
            task = {'id':task[0],'title':task[1],'description':task[2],'due_date':task[3],'status':task[4]}
            cursor.close()

        except TypeError:
            return JsonResponse({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)  
        
        except Exception as e:
            return JsonResponse({"error": f"{e}"}, status=status.HTTP_417_EXPECTATION_FAILED)  
        
        
        return JsonResponse(data=task , status = status.HTTP_200_OK)


def validate_due_date(date_str):
    """
    Validate due_date format (YYYY-MM-DD).
    Return the formatted date string if valid,
    otherwise raise a ValueError.
    """
    try:
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")  
        return valid_date.strftime("%Y-%m-%d")  # normalize format
    except ValueError:
        raise ValueError("Invalid due_date format. Use YYYY-MM-DD.")