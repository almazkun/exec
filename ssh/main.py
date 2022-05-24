import os
from fabric import Connection
from logging import getLogger


logger = getLogger(__name__)

HOST = os.environ.get("HOST")
USER = os.environ.get("USER_NAME")
KEY_FILENAME = os.environ.get("KEY_FILENAME")


class SSHClient:
    def __init__(self, host: str, user: str, key_filename: str):
        self.host = host
        self.user = user
        self.key_filename = key_filename
        print(f"SSHClient.__init__(): {self.host}, {self.user}, {self.key_filename}")

    def connection(self) -> Connection:
        logger.info(
            f"SSHClient.connection(): {self.host}, {self.user}, {self.key_filename}"
        )
        import os

        logger.info(f"key exists: {os.path.exists(self.key_filename)}")
        return Connection(
            self.host,
            user=self.user,
            port=22,
            connect_kwargs={
                "key_filename": self.key_filename,
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
    print("should be key:", key, end=" -> ")
    client.run(f"echo ${key}")


def main():
    ssh = SSHClient(
        host=HOST,
        user=USER,
        key_filename=KEY_FILENAME,
    )
    with ssh.connection() as client:
        client.config.run.env = env_variables

        [env_echoer(client, key) for key in env_variables.keys()]

        for command in command_pipeline:
            client.run(command)


if __name__ == "__main__":
    main()
