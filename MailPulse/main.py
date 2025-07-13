from fastapi import FastAPI
from ai import mail_summarizer

app = FastAPI()

@app.get("/")
def nika ():
    return f"{"Hello world"}"

@app.get("/mails")
def mail ():
    dm_mail = mail_summarizer()
    return f"This is your summary{dm_mail}"