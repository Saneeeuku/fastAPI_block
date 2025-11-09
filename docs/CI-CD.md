# Настройка CI/CD
### 1. Создать runner для проекта:
#### Запуск раннера
```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```
#### Регистрация раннера
```bash
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register
```
#### Изменение конфига
1. Редактируем конфиг по пути
`/srv/gitlab-runner/config/config.toml`        
2. Меняем      
`volumes = ["/cache"]` на \
`volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]`
### 2. Создать template пайплайна (напр. на сайте Gitlab)
### 3. Внести переменные окружения на сайте Gitlab
### 4. Оптимизация docker-compose.yml для СI 
Убрать env из сервисов, переписать image на image из .gitlab-ci.yml
