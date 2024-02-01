from api_platforma_ofd import AsyncClient
import asyncio
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import psycopg2 as pg
import json
import uvicorn
from datetime import datetime as dt, timedelta as td

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
def get_token():
    curs = db.cursor()
    curs.execute("""select
  json_agg(json_build_object('client_name', c.name, 'client_id', c.id, 'token', t.token))
from client_token t
left outer join client c on c.id=t.client_id""")
    answer = curs.fetchone()
    print(answer[0])
    return Response(content=json.dumps(answer[0]), media_type='application/json')


@app.get('/kkts')
async def kkts(token):
    kkts = await api.kkts(token=token)
    print(kkts)
    return kkts


@app.get('/receipts')
async def receipts(token, rnm: str, dateFrom: dt | None = dt.now() - td(days=1), dateTo: dt | None = dt.now()):
    receipts = await api.receipts(token=token, rnm=rnm, dateFrom=dateFrom, dateTo=dateTo)
    print(receipts)
    return receipts


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8800)
