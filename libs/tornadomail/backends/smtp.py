"""SMTP email backend class."""
from .. import smtplib
import socket

from .base import BaseEmailBackend
from ..utils import DNS_NAME
from ..message import sanitize_address

from tornado import gen


class EmailBackend(BaseEmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or '127.0.0.1'
        self.port = port or 25
        self.username = username or None
        self.password = password or None
        if use_tls is None:
            self.use_tls = None
        else:
            self.use_tls = use_tls
        self.connection = None
        self.template_loader = kwargs.get('template_loader', None)

    @gen.engine
    def open(self, callback):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            callback(False)
        try:
            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            self.connection = smtplib.SMTP(self.host, self.port,
                                           local_hostname=DNS_NAME.get_fqdn())
            yield gen.Task(self.connection.connect, self.host, self.port)
            if self.use_tls:
                yield gen.Task(self.connection.ehlo)
                yield gen.Task(self.connection.starttls)
                yield gen.Task(self.connection.ehlo)
            if self.username and self.password:
                yield gen.Task(self.connection.login, self.username, self.password)
            callback(True)
        except:
            if not self.fail_silently:
                raise

    def close(self):
        """Closes the connection to the email server."""
        try:
            try:
                self.connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.connection.close()
            except:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None

    @gen.engine
    def send_messages(self, email_messages, callback=None):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return

        new_conn_created = yield gen.Task(self.open)
        if not self.connection:
            # We failed silently on open().
            # Trying to send would be pointless.
            return
        num_sent = 0
        for message in email_messages:
            sent = yield gen.Task(self._send, message)
            if sent:
                num_sent += 1
        if new_conn_created:
            self.close()
        if callback:
            callback(num_sent)

    @gen.engine
    def _send(self, email_message, callback=None):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            if callback:
                callback(False)
        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]
        try:
            yield gen.Task(self.connection.sendmail, from_email, recipients,
                    email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            if callback:
                callback(False)
        if callback:
            callback(True)
