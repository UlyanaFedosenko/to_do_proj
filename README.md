# RESTful API - ToDo list


## Prerequisites
Befor running the bot, ensure you have the following installed:
- Python 3x
- Docker

## Getting Started
1. Clone the repository:

        git clone https://github.com/UlyanaFedosenko/to_do_proj.git

        cd to_do_app

2. Build the Docker image:

        docker build -t to-do-app .  


## Running the Server
Run the Docker-compose with the following comand:

    docker-compose up

use the following address - http://0.0.0.0:5002/

## API Endpoints
1. User Registration
   
        URL: /register
   
        Method: POST
   
        Payload: JSON object containing user details (first name, last name, username, password)
   
        Response: JSON object with a success or error message
   
2. User Login

        URL: /login
   
        Method: POST
   
        Payload: JSON object containing username and password
   
        Response: JSON object with an access token or an error message
   
3. Create Task:

        URL: /task
   
        Method: POST
   
        Payload: JSON object containing task details (title, description, status)
   
        Response: JSON object with a success or error message
   
4. Get All Tasks:

        URL: /tasks
   
        Method: GET
   
        Response: JSON object containing a list of tasks
   
5. Get User Tasks:

        URL: /tasks/<int:user_id>
   
        Method: GET
   
        Response: JSON object containing a list of tasks for the specified user
   
6. Get Task by ID:

        URL: /tasks/<int:task_id>
   
        Method: GET
   
        Response: JSON object containing the task details
   
7. Update Task:

        URL: /tasks/<int:task_id>
   
        Method: PUT
   
        Payload: JSON object containing updated task details
   
        Response: JSON object with a success or error message
   
8. Delete Task:

        URL: /tasks/<int:task_id>
   
        Method: DELETE
   
        Response: JSON object with a success or error message
   
9. Mark Task Completed:

        URL: /tasks/<int:task_id>/complete

        Method: PATCH
   
        Response: JSON object with a success or error message
   
10. Filter Tasks by Status:

        URL: /tasks/
    
        Method: GET
    
        Query Parameters: status (accepted values: 'NEW', 'IN PROGRESS', 'COMPLETED')
    
        Response: JSON object containing a list of tasks filtered by the specified status
