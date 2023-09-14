
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

docker-compose -f ../docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f ../docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear