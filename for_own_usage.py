from api_platforma_ofd import AsyncClient
import asyncio
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import psycopg2 as pg
import json
import uvicorn

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = AsyncClient()

db = pg.connect('postgres://ofd_admin:helloKitty@192.168.1.108:4000/ofd')


@app.get('/clients')
def get_token(client_id):
    curs = db.cursor()
    curs.execute("""select
  json_agg(json_build_object('client_name', c.name, 'client_id', c.id, 'token', t.token))
from client_token t
left outer join client c on c.id=t.client_id""")
    answer = curs.fetchone()
    answer = answer[0]
    res = []
    for i in answer:
        if (i['client_id'] == client_id):
            print(i['token'])
            res.append(i['token'])
    return res
    print(res)


@app.get('/kkts')
async def kkts(token):
    kkts = await api.kkts(token=token)
    print(kkts)
    return kkts


@app.get('/receipts')
async def receipts(token):
    receipts = await api.receipts(token=token)
    print(receipts)
    return receipts


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
