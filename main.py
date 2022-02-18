from fastapi import FastAPI

import book

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/api/gym/book')
async def book_gym():
    await book.book_next_hour_slot()
    return {'message': 'Successfully booked the gym slot and sent email'}    

