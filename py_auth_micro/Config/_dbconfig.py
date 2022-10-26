from dataclasses import dataclass
import ssl


@dataclass
class DBConfig:
    """A Class holding our Database configuration

    This Class holds our Database Configuration and has a function to get a TortoiseORM compliant connection String or a dictionary

    Attributes:
        database (str): Name of the Database which should be used.
        user (str): Username for the Database connection.
        host (str, optional): IP or DNS Hostname of the Database Server. Defaults to "127.0.0.1".
        port (int, optional): Port of the Database Server. Defaults to 3306.
        ca_file (str, optional): Path to an ca file. If specified it will create an ssl context. Defaults to None.
    """

    database: str
    user: str
    password: str
    host: str = "127.0.0.1"
    port: int = 3306
    ca_file: str = None

    @property
    def sslcontext(self):
        """if a ca_file is specified this is an :code:`SSLContext` else it is None"""
        if self.ca_file is None:
            return None

        return ssl.create_default_context(cafile=self.ca_file)

    @property
    def connection_string(self):
        """str: Connectionstring for tortoise ORM using the specified Values"""
        return f"mysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def to_dict(self, connection_name: str = "default") -> dict:
        """This Function generates a TortoiseORM compliant Database Connection dict

        Pass the Result of this Function into the `connections` Part of you Tortoise ORM
        config dict.

        Args:
            connection_name (str, optional): Name of this Database Connection. Defaults to "default".

        Returns:
            dict: Tortoise ORM Compliant dictionary Config (at least for the `connections` section)
        """
        return {
            connection_name: {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "database": self.database,
                    "host": self.host,
                    "password": self.password,
                    "port": self.port,
                    "user": self.user,
                    "ssl": self.sslcontext,
                },
            }
        }
