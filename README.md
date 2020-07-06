# Description
In this project, we will play the game of Halma, an adversarial game with some similarities to checkers. The game uses a 16x16 checkered gameboard. Each player starts with 19 game pieces clustered in diagonally opposite corners of the board. To win the game, a player needs to transfer all of their pieces from their starting corner to the opposite corner, into the positions that were initially occupied by the opponent. Note that this original rule of the game is subject to spoiling, as a player may choose to not move some pieces at all, thereby preventing the opponent from occupying those locations. Note that the spoiling player cannot win either (because some pieces remain in their original corner and thus cannot be used to occupy all positions in the opposite corner). Here, to prevent spoiling, we modify the goal of the game to be to occupy all of the opponent’s starting positions which the opponent is not still occupying.

# Setup

# Play Sequence
We first describe the typical play for humans. We will then describe some minor modifications for how we will play this game with artificial agents.
- Create the initial board setup according to the above description.
- Players randomly determine who will move first.
- Pieces can move in eight possible directions (orthogonally and diagonally).
- Each player's turn consists of moving a single piece of one's own color in one of the
following plays:
- One move to an empty square:
 - Move the piece to an empty square that is adjacent to the piece’s original position (with 8-adjacency).
 - This move ends the play for this player’s turn.
          
- One or more jumps over adjacent pieces:
 - An adjacent piece of any color can be jumped if there is an empty square
on the directly opposite side of that piece.
 - Place the piece in the empty square on the opposite side of the jumped
piece.
 - The piece that was jumped over is unaffected and remains on the board.  - After any jump, one may make further jumps using the same piece, or end
the play for this turn.
 - In a sequence of jumps, a piece may jump several times over the same
other piece.
- Once a piece has reached the opposing camp, a play cannot result in that piece leaving
the camp.
- If the current play results in having every square of the opposing camp that is not already
occupied by the opponent to be occupied by one's own pieces, the acting player wins. Otherwise, play proceeds to the other player.
Below we show examples of valid moves (in green) and invalid moves (in red). At left, the isolated white piece can move to any of its empty 8 neighbors. At right, the central white piece can jump over one adjacent piece if there is an empty cell on the other side. After one jump is executed, possibly several other valid jumps can follow with the same piece and be combined in one move; this is shown in the sequence of jumps that start with a down-right jump for the central piece. Note that additional valid moves exist that are not shown (e.g., the central white piece could move to some adjacent empty location).


Note the invalid moves: red arrow going left: cannot jump over one or more empty spaces plus one or more pieces. Red arrow going left-down: cannot jump over one or more pieces plus one or more empty spaces. Red arrow going down: cannot jump over more than one piece.
