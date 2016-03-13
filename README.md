# botnets-longrun

How to run:
```
virtualenv env
source env/bin/activate
make run
```

Le programe utilise Celery pour démarer des tâches qui vont chercher des images.
Une tâche est démarrée par mot clé.

Le programme utilise OAUTH. Pour créer un utilisateur:
 - curl -i -X POST -H "Content-Type: application/json" -d '{"username":"csgames","password":"csgames"}' http://127.0.0.1:5000/api/users

On peux ensuite obtenir un token:
 - curl -u csgames:csgames -i -X GET http://127.0.0.1:5000/api/token

On peux finalement obtenir une liste d'images ainsi:
 - curl -u $TOKEN:unused --data "text=potato" http://localhost:5000/api/images
