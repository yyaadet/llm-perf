#!/bin/sh

cookie='Oasis-Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3RpdmF0ZWQiOnRydWUsImFnZSI6NywiYmFuZWQiOmZhbHNlLCJleHAiOjE3MTE0NTgwOTQsIm1vZGUiOjIsIm9hc2lzX2lkIjo4MzgzNTg3ODQwOTE3NTA0MCwidmVyc2lvbiI6MX0.c1ej2Clk--mTaif92EF6MNJkYe7DSxYj1-Kk5bBX8OU...eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOjEwMjAwLCJkZXZpY2VfaWQiOiIzMjVmODFlMmM3ZmI0ODg5Y2RmYWRiMWVjMGI1YjNmNWVhMTlhZjkyIiwiZXhwIjoxNzEyNzM3MzU1LCJvYXNpc19pZCI6ODM4MzU4Nzg0MDkxNzUwNDAsInZlcnNpb24iOjF9.VjPbmnERAiECyDhheqcwGvVZvTVsWHVOEmrZH-K-aPw; Oasis-Webid=325f81e2c7fb4889cdfadb1ec0b5b3f5ea19af92'
chat_id='83885550012493824'
appid="10200"

python run.py step\
  --cookie "${cookie}" \
  --token "${token}" \
  --chat_id "${chat_id}" \
  --appid "${appid}"
