# model data backend
 
To get the Redis server running: 

1. Make sure you have installed Docker. 

2. `docker pull redis`

3. `docker run --name redis-server -d -p 6379:6379 redis`

4. `docker ps` (check if the server is running)

5. `docker exec -it redis-server redis-cli`

6. `docker stop redis-server` (when needed)





