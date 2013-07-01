from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test kindress')
    local('git add -p && git commit')

def deploy():
  with lcd('/srv/www/kindress/'):
    local('git pull git@github.com:varl/kindress.git')
    local('python manage.py test kindress')
    # local('/my/command/to/restart/webserver')
