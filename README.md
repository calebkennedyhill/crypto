# crypto
Jeremy Juybari and Caleb Hill learn number theory and cryptography. We'll see where this goes...

# Docker

Steps to install Docker. Information [here](https://docs.docker.com/engine/install/)
I installed only Docker Engine and not Docker Desktop (includes a VM, we can do everything we need with the Engine-could be wrong).

See the link and click on your OS. I installed using the apt repo on Ubuntu. 
Verify everything working: 

```bash
sudo docker run hello-world
```
You need to run as root. 
## Docker Hello
To get a simple docker container to run a python command do the following:
1) Make a Dockerfile with the following,
```docker 
FROM python:3.15-trixie
RUN useradd --create-home appuser # non root user in container
USER appuser
CMD ["python", "-c", "print('Hello World')"]
```
2) then do ```bash sudo docker build -t py-hello .``` This will take about a minute for the first time. 
3) sudo docker run py-hello

If you are looking for the image files, they are handled by docker and stored in /var/lib/conatinerd/
