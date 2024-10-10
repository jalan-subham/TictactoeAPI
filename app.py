from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from tictactoefunctions import *

app = FastAPI()

@app.get('/getNextMove')
def get_items(board: str, firstmove: str):
    board = list(map(int, board.split(',')))  # Convert the CSV string to a list of integers
    print(board)
    # Retrieve the 'firstmove' parameter and convert it to a boolean
    firstnextmove = firstmove.lower() == "true"  # Convert "True" or "False" to a boolean
    move = computer_move(board,firstnextmove)
    ret_response = jsonable_encoder({"move":f"{move}"})
    return JSONResponse(content=ret_response)

@app.get("/")
def index():
    return JSONResponse(jsonable_encoder({"message": "nothing here"}))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)