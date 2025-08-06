from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

# Create your views here.

def home(request):
    
    # Creating Tasks Through Post Requests
    #  
    if request.method == 'POST':
        data = request.POST
        title = data['title']
        description = data['description']
        due_date = data['due_date']
        status = data['status']

        with  connection.cursor() as cursor:
            cursor.execute("INSERT INTO tasks(title,description,due_date,status) VALUES(%s,%s,%s,%s)",
                           [title, description , due_date, status  ]
                           )
            cursor.close()
            messages.success(request,"Created a Task Succefully")
            return redirect('home')
        
    # showing all the listed task     
    with connection.cursor() as cursor:
        cursor.execute("SELECT id , title , description , due_date , status FROM tasks")
        tasks_data = cursor.fetchall()
        
        # here i am coverting the task_data from a tuple list to dict list with key value

        tasks = [{'id':task[0] ,'title':task[1] , 'description':task[2] , 'due_date':task[3] ,'status':task[4]   } for task in tasks_data]
        cursor.close()
    
    
    return render(request ,'index.html'  , context={'all_tasks':tasks})

def delete_task(request , task_id):
    

    with connection.cursor() as cursor:
        sql_query = "DELETE FROM tasks WHERE id=%s"
        task_to_delete = (task_id,)
        cursor.execute(sql_query , task_to_delete)
        connection.commit()
        cursor.close()
        messages.success(request,f"Deleted The Task Succefully Task no-{task_id}")
    return redirect('home')

def update_task(request , task_id , status):
    if status == 'Progress':
        status = 'In Progress'

    with connection.cursor() as cursor:
        sql_query = "UPDATE tasks SET status=%s WHERE id=%s "
        task_to_update = (status , task_id) 
        cursor.execute(sql_query , task_to_update)
        connection.commit()
        cursor.close()
        messages.success(request,f"Updated The Task  Status Succefully as {status} Task no-{task_id} ")
    return redirect('home')    
    



