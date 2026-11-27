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

## Docker data

You need to make the data dir and sub dirs
```bash
mkdir -p ./trade/data/raw/
mkdir -p ./trade/data/output/
```

```bash
sudo docker build -f ./docker/Dockerfile.data -t downloader .

```

```bash
sudo docker run -v "$(pwd)/trade/data/raw:/app/raw:rw" --rm downloader &

```
The first part is the host dir and the second part is the dir in the container
& is so the shell is returned. You can see what container is running with sudo docker ps
sudo docker images shows all of the built images. The --rm does not delete the image file rather
just the container which you can think of as instance of the image file.

```bash
sudo docker run --rm -it downloader bash
```
if you want to poke around in the container. 

There were some design choices that we could change. I had the dir in the container not match the dir on the host
I'm not sure if this over complicates things or not. Additionally, uv is not fully being used in the caching. I think we install everything on the host and we can sync. I'm not sure. 