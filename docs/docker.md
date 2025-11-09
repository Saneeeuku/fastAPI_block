# Docker команды для проекта
### Создание Docker сети
```bash
docker network create my_network
```
### База данных
```bash
docker run --name booking_db -p 6432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=booking \
  --network=my_network \
  --volume pg_booking_data:/var/lib/postgresql \
  -d postgres:18.0
```
### Nginx
! Для запуска на windows необходимо указывать полный путь для volume (например --volume //c/Users/user/project/nginx.conf:/etc/nginx/nginx.conf)

Без SSL (http)        
```bash
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=my_network \
    --rm -p 80:80 nginx
```
С SSL (https)        
```bash
docker run --name booking_nginx \
--network=my_network \
--volume ./nginx.conf:/etc/nginx/nginx.conf \
--volume /etc/letsencrypt:/etc/letsencrypt \
--volume /var/lib/letsencrypt:/var/lib/letsencrypt \
--rm -p 80:80 -p 443:443 nginx
```