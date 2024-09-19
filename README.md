```bash
sudo docker build .
sudo docker-compose up -d
sudo docker-compose exec web python3 -m scripts.on_start
sudo docker-compose exec web python3 -m pytest app/tests/
```
