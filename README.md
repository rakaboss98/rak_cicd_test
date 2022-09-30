# Important steps and commands
This repository is a simple example of implementing a CICD process using GitHub Actions, Amazon ECR, Amazon EC2 and bash scipt
## Structuring the repository on the local
The repository consists of the following files, the functionality of each of them is specified

* dataloader: Pulls & Pushes data from and to S3 respectively
* func.py: Simple function that takes a csv file and performs addition of two coloumns 
* app.py: Fastapi app that spins up a server to take input from cutomer, process data using func and update the database
* Dockerfile: Creates a docker environment in EC2 with all the necessary dependencies required to run the repository
* docker-compose.yml: Automates the build and run of dockerfile (not used in this project)
* Data: A folder which stores the data for func in EC2
* rak_cicd_test.yml: Github actions workflow that builds the docker image from Dockerfile, pushes it to Amazon ECR and starts an EC2 Container

## Configure Github actions 

* Just add the aws_access_id, aws_secret_access_key and EC2 instance ID in github secrets, the rak_cicd_test.yml will automatically run on git push and update image in ECR
* Make sure your user has an access to push to ECR, if not, give access in AWS->IAM->Users

## Pull the image to EC2

There are multiple steps required to configure your EC2 instance to make sure the CICD pipeline works seamlessly

### Create an Elastic IP and assign it to your instance 

* AWS instance changes its public IP address on reboot, which creates difficulty in creating a proxy pass
* To avoid this, create a elastic IP address in AWS and assign it your EC2 instance, Now your public IP address will be fixed to this elastic IP address 

### Create an nginx proxy server 

A proxy server maps the EC2 port 80 to the active port of the local server, in this case the fastapi server, to create a proxy server execute the following steps:

First add the inbound rules in security groups to allow port 80 to take input requests, you can refer to this link: https://www.youtube.com/watch?v=UQLWYy-EpCg

Install nginx in your EC2 by executing the following commands 
```
sudo apt-get update
sudo apt-get install nginx
```
After nginx installation crete the following file:

```
sudo nano /etc/nginx/sites-enabled/fastapi_nginx 
```

Then add the following script: 
```
server{
        listen 80; # aws inbound ports
        server_name <put aws public IP address>;
        location / {
                proxy_pass http://127.0.0.1:8000; #fastapi local server address
        }
}
```

After saving the script, execute the following command (you can also add it to your automation bash script)

```
sudo service nginx restart
```
Your nginx proxy server is ready now 

### Configure awscli 

In order to make sure that you're able to pull the docker image from AWS ECR, you need to configure AWS command line interface, execute the following steps:
Install AWS cli
```
sudo apt-get install awscli
sudo aws configure
```
Add all your credentials in sudo aws configure


### Configure awscli & docker

If your EC2 instance does not have docker, you can install docker using the following command:

```
sudo apt-get install docker.io
```

Give permissions to docker to pull image from ECR

```
sudo aws ecr get-login-password --region <region_name> | sudo docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region_name>.amazonaws.com
```

### Create an bash automation script to automate docker pull and run processes

Now we'll create an automate.sh script to automate the actions that we need to run once the EC2 instance is started by Github actions 

```
#! /bin/sh
sudo service nginx restart
sudo docker pull <aws_account_id>.dkr.ecr.<your region>.com/<repo_name>:<tag>
sudo docker run -it -p 8000:8000 <aws account id>.dkr.<region name>.amazonaws.com/<repo name>:<tag> 
#etc.
```
Make sure  you've the permissions to run the bash script

Now Put this script in crontab to execute it whenever the instance gets started

```
crontab -e 
```

and add

```
@reboot /ubuntu/home/automate.sh
```
Now save and stop the container, make a change in your repository and push it to github
