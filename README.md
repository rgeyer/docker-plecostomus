# docker-plecostomus
Garbage collector for exited containers and dangling images

## Usage
It only works one way right now.

```
docker build -t docker-plecostomus .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock:ro -v `pwd`:/code -it docker-plecostomus python /code/main.py
```
