#TODO-LIST

To run locally :-

1. Create virtual environment
    python3 -m venv todo-env

2. Activate the virtual environment 
    \todo-env\Scripts\activate

3. Install depedencies
    pip install -r requirements.txt

4. Run the application 
    python app.py




To run in Docker:-

1. Go to the directory and build the docker image 
    docker build -t todo-list .

2. Run the container
    docker run -p 5000:5000 todo-list (This will start a container and map port 5000 on your host machine to port 5000 inside the container)



Api endpoints
1. Create task - http://localhost:5000/task (post)
2. Get all tasks - http://localhost:5000/tasks (get)
3. Get single tasks - http://localhost:5000/task/<id> (get)
4. Update a task - http://localhost:5000/task/<id> (put)
5. Delete a task - http://localhost:5000/task/<id> (delete)
6. Mark complete - http://localhost:5000/task/complete/<id> (put)
7. Mark incomplete - http://localhost:5000/task/incomplete/<id> (put)

