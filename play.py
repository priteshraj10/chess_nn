import torch
import random
import time
import chess.svg
from train import Net
import numpy as np
from state import State

from flask import Flask, Response
app = Flask(__name__)


class Valuator(object):
    def __init__(self):
        vals = torch.load('nets/value.pth', map_location=lambda storage, loc: storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, s):
        brd = s.serialize()[None]
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])


def explore_leaves(s, v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        ret.append((v(s), e))
        s.board.pop()
    return ret


# Chess board and "engine"
v = Valuator()
s = State()


def computer_move():
    move = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)[0]
    print(move)
    s.board.push(move[1])


@app.route("/")
def hello():
    ret = '<html><head>'
    ret+=  '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
    ret+= '<style> button { font-size: 30px; }</style>'
    ret+= '</head><body>'
    ret+= '<img width=600 height=600 src="/board.svg?%f"></img><br/>' % time.time()
    ret+= '<button onclick =\'$.post("/move"); location.reload();\'>Make  computer move</button>'
    return ret


@app.route("/board.svg")
def board():
    # computer move
    return Response(chess.svg.board(board=s.board), mimetype='image/svg+xml')


@app.route("/move", methods=["POST"])
def move():
    computer_move()
    return ""


if __name__ == '__main__':
    app.run(debug=True)

"""     
        # self play
        while not s.board.is_game_over():
            l = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)
            move = l[0]
            print(move)
            
        print(s.board.result())
"""