from flask import Flask, jsonify, request
from tictactoefunctions import *

app = Flask(__name__)




# Route to get all items
@app.route('/getNextMove', methods=['GET'])
def get_items():
    board_str = request.args.get("board")
    board = list(map(int, board_str.split(',')))  # Convert the CSV string to a list of integers
    print(board)
    # Retrieve the 'firstmove' parameter and convert it to a boolean
    firstnextmove_str = request.args.get("firstmove")
    firstnextmove = firstnextmove_str.lower() == "true"  # Convert "True" or "False" to a boolean
    move = computer_move(board,firstnextmove)
    return  jsonify({"move":f"{move}"}),200


