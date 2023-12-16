# Todo-Organizer

todo-organizer is a program to organize your todo-lists.
It is written in python and is optimized to be used within kubernetes.

## Installation
### Install on kubernetes
A helm chart can be found in the *helm* directory. Before installing it the dependencies need to be build, this can be done with `helm dependencies build`, after that the chart can be installed with `helm upgrade --install <insert_name> .`. For available settings-option please consult the *values.yaml* file.
### Install on docker
When running on docker you have to handle the database setup yourself.
To set the connection string you have to set env-var `DB_CONNECTION_STRING`. It is recommended to use a separate database, e.g. postgres. 
However to use a local sqlite database you set it to 
`sqlite+pysqlite:///test`.
If you use a database inside the docker container ensure to mount it in a volume to preserve its data.
In addition to provide the connection string you also have to handle the upgrade/initialization of the tables. This is done by executing the following command

```bash
alembic upgrade head
```

Here is an example docker compose file that does all of the above:
```yaml
services:
  todo-organizer:
    image: "ghcr.io/melvinkl/todo-organizer:7"
    volumes:
      - ./database.sqlite:/database.sqlite
    environment:
      - DB_CONNECTION_STRING=sqlite+pysqlite:///database.sqlite
    entrypoint:
      - /bin/sh
      - -c
      - |
        alembic upgrade head
        streamlit run main.py --server.port=8080 --server.address=0.0.0.0
    ports:
      - 8080:8080
```
When using this docker-compose file, the todo-organizer service can be reached at `localhost:8080`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
