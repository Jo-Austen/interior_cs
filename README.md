# interior_cs
For Comapny

Branch Routing

push main/master → deploy to production

push other branches → deploy to test

pull_request → CI only, no deploy

Endpoints

test: http://SERVER:8081 (health: /health)

prod: http://SERVER:8080 (health: /health)