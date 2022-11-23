"""
Implement a chess player based on the python-chess library, which we put
into your repository. The player should use UCT to get the best move. Use
the ChessNode tree structure to build the tree and search in it.

The chess player has one local board on which moves can be simulated
without playing them on the official board:

    board.simulate_move(move)

To simulate all moves which correspond to one particular node in the tree
you can call:

    board.simulate_moves_from_node(node)

Since this local board is reused for all nodes, you have to reset it after
you simulated moves on it:

    board.reset_simulated_moves()


Some more examples of the use of python-chess:

To randomly choose a move from all legal moves you can do:

    random.choice([m for m in board.legal_moves])

This generates a list from all legal_moves (which is a generator object
and can only be iterated over) and than randomly chooses one of the entries.


You can check for a terminal state of a board with:

    board.is_game_over()

And for checkmate with

    board.is_checkmate()

Thus you can check who won with e.g.:

    if board.is_checkmate():
        if board.turn == player:
            pass  # checkmate and players turn -> opponent wins
        else:ggg
            pass  # checkmate and opponents turn -> player wins
    elif board.is_game_over():
        pass  # draw


Make sure your implementation works for both
player == chess.WHITE and player == chess.BLACK
"""

from __future__ import division
import chess
import random
import math
from evaluation import evaluation

rechentiefe = 5

class ChessPlayer(object):
    """
    A chess player class that uses a Monte-Carlo tree search to get the
    next best move. The basic structure is already implemented for you,
    so that you don't have to care about pruning away parts of the tree
    and updating the root after each move.
    """
    def __init__(self, board, player):
        self.player = player
        self.board = board
        self.root = ChessNode(self.board, None, None)

    def inform_move(self, move):
        self.board.push(move)
        if move in self.root.untried_legal_moves:
            self.root = ChessNode(self.board, None, move)
        else:
            for child in self.root.children:
                if child.move == move:
                    self.root = child
                    self.root.parent = None
                    break

    def get_next_move(self):
        """
        Generates moves until a time limit is reached.
        The last move generated within the limit will be the move
        you officially play.
        """
        while len(self.root.untried_legal_moves) > 0:
            y = self.root.expand(self.board)
            r = y.default_policy(self.player, self.board, rechentiefe)
            y.backup(self.player, r)
        
        while True:
            # I M P L E M E N T   U C T   H E R E
            
            nodeToExpandNext = self.root.tree_policy(self.board, self.player)
            
            #Diese if ist hier ausschliesslich zur Fehlerbehandlung, damit falls wir nicht mehr dazu kommen alles zu fixen, 
            #trotzdem kein fehler auftritt, und er halt einfach nicht weiterrechnet (das ist oke da der Fehlerfall extrem selten ist)
            #und sich einen Zug spaeter vermutlich aufloest durch die Baumaktualisierung
            if len(nodeToExpandNext.untried_legal_moves) != 0:
                newLeaf = nodeToExpandNext.expand(self.board)
                #print "GOOD"
            
                #print "expand -----"
                
            
                #print "tree policy -----"
                rewardForNewLeaf = newLeaf.default_policy(self.player, self.board, rechentiefe)
            
                #print "backup -----"
                newLeaf.backup(self.player, rewardForNewLeaf)
            
            
             
            if self.player == chess.WHITE:
                out = sorted(self.root.children, key=lambda x:x.sum_of_rewards/x.number_of_rollouts)
            else:
                out = sorted(self.root.children, key=lambda x:x.sum_of_rewards/x.number_of_rollouts, reverse =True)
            #print self.root.children
            #print out[0].move
            # yield what appears to be the best move after each iteration
            yield out[0].move
            
class ChessNode(object):
    """
    A chess tree structure. We already put all legal moves in the
    self.untried_legal_moves list. You have to take care of removing
    moves from that list by yourself, when expanding the tree! Also
    self.number_of_rollouts and self.sum_of_rewards is not automatically
    updated.
    """
    def __init__(self, board, parent, move):
        self.parent = parent
        self.move = move
        self.children = []
        self.number_of_rollouts = 0.
        self.sum_of_rewards = 0.

        board.simulate_moves_from_node(self)
        self.untried_legal_moves = [move for move in board.legal_moves]
        self.is_game_over = board.is_game_over()
        self.turn = board.turn
        board.reset_simulated_moves()
        #print 
        #print self.turn
        #print len(self.untried_legal_moves)
        #for x in self.untried_legal_moves:
        #    print x
        
    def move_history(self):
        """
        Generator for the moves that lead to this node
        """
        if self.parent is not None:
            for move in self.parent.move_history():
                yield move
            if self.move is not None:
                yield self.move

    def add_child(self, node):
        self.children.append(node)

    def backup(self, player, reward):
        """
        Backup the current counts and rewards after a rollout
        :param player: The player you are (either chess.WHITE or chess.BLACK)
        :param reward: Reward earned in a rollout
        """
        #pass
        
        if player == self.turn:
            self.sum_of_rewards += reward
        else:
            self.sum_of_rewards -= reward
        
        self.number_of_rollouts += 1
        
        if self.parent != None:
            self.parent.backup(player, reward)

    def best_child(self, beta=1): # =1 entfernen
        """
        Return the best child of this node.

        :param beta: The constant beta from the UCB algorithm
        :return: A ChessNode
        """
        #pass
        N = self.number_of_rollouts
        if N == 0:          
            return None     
            
        #hilfsvariable
        tmp = -1e100
        best = None
        
        for child in self.children:
            #Falls irgendein node, zwar noch viele pfade hat, aber alle schon expandet wurden (mindestens einmal)
            #sorgt die zweite if-Bedingung hier dafuer, dass dieser Pfad konstant ignoriert wird, da er niemals als best_Child returned werden kann
            #deshalb vielleicht in der treepolicy abfragen?
            if child.is_game_over or len(child.untried_legal_moves) == 0:           #!!!
                continue                     #!!!
            n = child.number_of_rollouts
            Q = child.sum_of_rewards
            ucb = (Q/n) + beta*math.sqrt((2*math.log(N))/n)
            
            #immer true, nur hilfsvariable
            if ucb > tmp:
                tmp = ucb
                best = child
        
        return best
    
    def tree_policy(self, board, player):
        """
        Return the most promising node to expand from this subtree.
        :param board: The players local board
        :return: A ChessNode
        """
        #pass
        best = self.best_child(beta = 1)
        
        #expandet falls der rollcounter zu gross wird 
        #funktioniert wie ein Filter. Sobald er beim durchiterieren merkt, mein Pfad wurde schon echt oft gerollt
        #probiere neue Zuege
        #man koennte hier auch anstatt > ein % also Modulo verwenden, finde die Idee sogar besser
        
        #if self.number_of_rollouts > 3:
        if len(self.untried_legal_moves) != 0:
                
                #nur ein neues node (Ergebnis moderat) mit > 10
                #print "ROLLER"
                #y = self.expand(board)
                #r = y.default_policy(player, board, rechentiefe)
                #y.backup(player, r)
                
                #alle (Ergebnis sehr schlecht) mit > 10
            while len(self.untried_legal_moves) > 0:
                y = self.expand(board)
                r = y.default_policy(player, board, rechentiefe)
                y.backup(player, r)
        
           
        if best != None:
            if not best.is_game_over:
                return best.tree_policy(board, player)
                
        #Hier ist der Fehler! in dieser if darf nicht self returned werden, aber auch nicht neu treepolicy augerufen werden...
        """Traceback (most recent call last):
        File "interface.py", line 246, in <module>
        main()
        File "interface.py", line 242, in main
        winner = simulate_game(players, board, args.secs)
        File "interface.py", line 177, in simulate_game
        board, move = play_move(board, secs, players[current])
        File "interface.py", line 142, in play_move
        tmp_move = next(move_generator)
        File "C:\Users\Erik-\Desktop\Neuer Ordner (2)\group_146\group_146\e02_uct\ex_uct.py", line 109, in get_next_move
        newLeaf = nodeToExpandNext.expand(self.board)
        File "C:\Users\Erik-\Desktop\Neuer Ordner (2)\group_146\group_146\e02_uct\ex_uct.py", line 253, in expand
        move = random.choice(self.untried_legal_moves)
        File "C:\Python27\lib\random.py", line 275, in choice
        return seq[int(self.random() * len(seq))]  # raises IndexError if seq is empty
        IndexError: list index out of range"""

        #hier dann eventuell random expansion von der root aus einleiten?
        #if len(self.untried_legal_moves) == 0:
            #print
            #print "ERROOOOOOOOOOOOR"
                
        return self
        
    def expand(self, board):
        """
        Expand this node with a random child and return the child node
        :param board: The players local board
        :return: A ChessNode
        """
        #pass      
        move = random.choice(self.untried_legal_moves)
        newChild = ChessNode(board, self, move)
        self.add_child(newChild)
        self.untried_legal_moves.remove(move)
        
        return newChild
        
    def default_policy(self, player, board, M):
        """
        Do a single rollout starting from this node and return a reward for the
        terminal state.

        If you recognize that a full rollout is too slow to get UCT running
        reasonably well, use the evaluation function in evaluation.py to cap
        the depth of the rollouts.

        If you are good at chess, you might as well write eyour own board-
        evaluation function.

        :param player: The player you are (either chess.WHITE or chess.BLACK)
        :param board: The players local board
        :return: reward
        """
        #pass
        mh = self.move_history()
        for move in mh:
            board.simulate_move(move)
        ##Random Rolleout
        for i in range(M):
            if board.is_checkmate() or board.is_game_over():
                break
            legalMoves = [m for m in board.legal_moves]
            simMov = random.choice(legalMoves)#
            board.simulate_move(simMov)
  
        reward = evaluation(board)   #error moeglichkeiten!!!!!!!!!!!!!
        board.reset_simulated_moves()
        
        return reward
