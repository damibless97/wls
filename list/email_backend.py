import ssl
from django.core.mail.backends.smtp import EmailBackend

class UnsafeEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        # Create an unverified SSL context (ignores bad certificates)
        context = ssl._create_unverified_context()

        # Provide default values if not set

        self.connection = self.connection_class(
            self.host,
            self.port,
            timeout=self.timeout,
            ssl_context=context,
        )
        self.connection.set_debuglevel(int(self.use_debugging_server))

        if self.username and self.password:
            self.connection.login(self.username, self.password)

        return True
