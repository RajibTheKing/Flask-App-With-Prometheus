## How to run Flask Application along with Prometheus metrics?
Firstly, docker should be installed in the system. As this is not the part of this demo, I am not going to show it here. Please follow documentation for docker installation. 

After installing docker, just run this three command.

```
docker build -t awesome-flask:latest .
docker-compose up -d
docker-compose ps
```

## How to access web interface?
 - Prometheos : http://localhost:9090
 - Flask Server: http://localhost:5000/metrics
 