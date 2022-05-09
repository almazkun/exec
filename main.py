import os
from fabric import Connection


class SSHClient:
    def __init__(self, host, user, key_filename):
        self.host = host
        self.user = user
        self.key_filename = key_filename

    def connection(self):
        return Connection(
            self.host,
            user=self.user,
            port=22,
            connect_kwargs={
                "key_filename": f"{self.key_filename}",
            },
            inline_ssh_env=True,
        )


command_pipeline = [
    "docker ps -a",
    "docker images",
]

env_variables = {
    "RABBITMQ_DEFAULT_USER": "RABBITMQ_DEFAULT_USER",
    "RABBITMQ_DEFAULT_PASS": "RABBITMQ_DEFAULT_PASS",
    "POSTGRES_USER": "POSTGRES_USER",
    "POSTGRES_PASSWORD": "POSTGRES_PASSWORD",
}


def env_echoer(client, key):
    print("should be key:", key)
    client.run(f"echo ${key}")


def main():
    ssh = SSHClient(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        key_filename=os.environ.get("KEY_FILENAME"),
    )
    with ssh.connection() as client:
        client.config.run.env = env_variables
        [env_echoer(client, key) for key in env_variables.keys()]
        for command in command_pipeline:
            client.run(command)


if __name__ == "__main__":
    main()
