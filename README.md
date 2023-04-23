# KRAKE

Krake wants to manage and connect thinks in Utopiastadt, /dev/tal, FabLab, ...

```
docker-compose up -d --build
docker-compose exec -w /app/krake django python manage.py makemigrations inventory
docker-compose exec -w /app/krake django python manage.py migrate
docker-compose exec -w /app/krake django python manage.py createsuperuser
```

http://localhost:8000/admin/