Goal: To deploy RAG application in EC2 as docker container and expose it

Prereq:

- Need EC2
- Need Docker installed on EC2 + Docker compose ( deploy-ec2.sh )

What does deploy-ec2.sh do?

- Updates system binary repository
- It installs docker engine
- It installs docker compose
- It clones github repo
- It sets .env ( open ai api key )
- It build docker image with help of docker compose
- It runs the container and attaches port 8501 to host ( ec2 machine )

## Scaling:

ELB -> Target Group -> Group of machines ( EC2 )
