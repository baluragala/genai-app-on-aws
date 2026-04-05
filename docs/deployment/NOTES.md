# Steps to deploy

1. Create EC2 machine with Amazon Linux and machine type as t3.medium, 20 GB Storage
2. Connect to machine using EC2Instance connect
3. Once connected create deploy-ec2.sh file using `nano deploy-ec2.sh`
4. make sh file execuatble by running `chmod +x deploy-ec2.sh`
5. run `./deploy-ec2.sh` ( do setup of git, docker, cloning you repo, enabling necessary persmission for ec2-user)
6. close cloud shell and start another EC2Instance connect
7. change director into you repo
8. run `./deploy-ec2.sh` ( it will build docker image and run the app)
9. Change security group of your EC2 machine to allow port 8501 in inbound rules
10. browse the app on http://your-ec2-public-ip:8501
