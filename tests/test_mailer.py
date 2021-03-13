import sys
import pytest
sys.path.append('..')
from mailer import send_plaintext_mail, send_html_mail

def test_mailer():
    send_plaintext_mail("testing testing")

def test_html_mailer():
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a>
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    #send_html_mail(html)