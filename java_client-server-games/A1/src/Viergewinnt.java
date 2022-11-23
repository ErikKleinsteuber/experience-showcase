import sun.awt.image.ImageWatched;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class Viergewinnt extends Spiel implements Protokolierbar {

    Scanner in = new Scanner(System.in);

    boolean patt = true;
    boolean running, wannaPlay;
    private LinkedList<int[]> moveHistory = new LinkedList<>();

    //alles private

    int drawingPlayer = 1;      //which players draw it is
    int moveCmd = -1;           //moveCommand for passing the moves


    //TODO: rekonstruiere Dialog so, dass man Viergewinnt oder Chomp separat starten kann

    public Viergewinnt() {

        //SETUP BEGIN
        initBoard();

        //Player name dialogue
        playerNmeDlg();

        //Set Field Size
        setFldSize();

        System.out.println("Let the games begin!\n");
        System.out.println("Player 1: " + playerOne.name + " VS Player 2: " + playerTwo.name);
        //SETUP END
        //kein print im konstruktor

        //ENTRY POINT
        gameLoop();
    }

    void gameLoop() {
        running = true;         //if round is running
        wannaPlay = true;       //checks if User wants to play another round

        board.initField();      //setup board
        board.displayBoard();

        //GAME LOOP
        while (wannaPlay) {             //starts new games while Player wants to play (without changing setup)
            while (running) {           //simulates passes while game is running
                simulatePass();                 //simulates pass (player 1 draws and then player 2)
            }
            System.out.println("GAME OVER.");

            if (patt == true) {
                System.out.println("PATT.");
            } else {
                System.out.println("WINNER IS " + winnerIs());
            }

            moveHistory().clear();              //clear history for a fresh new game
            System.out.println("Wanna play again? [y=1/n=else]?");
            try {
                if (in.nextInt() == 1) {
                    gameLoop();
                } else {
                    wannaPlay = false;
                }
            } catch (Exception e) {
                System.out.println("Wrong input. Closing Viergewinnt now, good-bye :)");
                wannaPlay = false;
            }

        }
    }

    @Override
    public LinkedList<int[]> moveHistory() {
        return moveHistory;
    }

    @Override
    public void logDraw(int moveCmd) {
        int[] x = new int[2];
        x[0] = drawingPlayer;
        x[1] = moveCmd;
        moveHistory().add(x);
    }

    @Override
    public void undoDraw() {
        int lastMove = moveHistory().pollLast()[1];
        for (int x = 0; x < board.boardSize.elementAt(1); x++) {
            if (board.field[x][lastMove] != 0) {
                board.field[x][lastMove] = 0;
                break;
            }
        }
    }

    @Override
    void playDraw(int moveCmd, int playerNumber) {
        System.out.println("Playing draw...");
        for (int x = board.boardSize.elementAt(0) - 1; x >= 0; x--) {

            if (board.field[x][moveCmd] == 0) {
                board.field[x][moveCmd] = drawingPlayer;
                break;
            }
        }
    }

    @Override
    void simulatePass() {

        //konstanten als moves möglich
        moveCmd = -1;           //resetting moveCommand
        boolean undo = false;   //if player wants to undo last draw

        //"Durchgang" roundloop (player 1 -> player 2)
        for (int x = 0; x < 2; x++) {

            //break if game over
            if (running == false) break;

            //Computer moves
            if (drawingPlayer == 2 && playerTwo.type == false) {

                //TODO: implement Computer drawing
                //System.out.println("BMO draws...");

                moveCmd = ThreadLocalRandom.current().nextInt(0, board.boardSize.elementAt(1) - 1);
            }

            //humans move
            while (checkIfMovePossible(moveCmd) == false) {
                System.out.println("Make a move Player " + drawingPlayer);

                try {
                    moveCmd = in.nextInt();
                } catch (Exception e) {
                    in.nextLine();
                }

                //removing draw
                if (moveCmd == -2 && !moveHistory().isEmpty()) {
                    undo = true;
                    break;
                }

                if (checkIfMovePossible(moveCmd) == false) System.out.println("Incorrect moveCommand. Try again!");
            }

            if (undo == true) {             //undo
                undoDraw();
                moveCmd = -1;
                undo = false;
                if (!playerTwo.type) {
                    undoDraw();
                    drawingPlayer = 2;
                    board.displayBoard();
                } else {
                    board.displayBoard();
                }
            } else {                        //drawing
                playDraw(moveCmd, drawingPlayer);
                board.displayBoard();
                logDraw(moveCmd);

                //check for game over of any kind
                validateGame(moveCmd);
            }

            //turn logic
            if (drawingPlayer == 1) {
                drawingPlayer = 2;
                x = 1;
            } else {
                drawingPlayer = 1;
                x = 2;
            }

            //printMoveHistory();

            moveCmd = -1;
        }
    }

    void validateGame(int moveCmd) {

        //chipHeight is the height at which the chip has been placed
        //it helps us calculating if the player who just drawed, made a winning move
        int chipHeight = 0;
        //calculating chipheight
        for (int x = 0; x < board.boardSize.elementAt(0); x++) {
            if (board.field[x][moveCmd] != 0) {
                chipHeight = x;
                break;
            }
        }


        //System.out.println("Chipheight = " + chipHeight);
        int winCondition = 0;

        //Checking from left to right
        for (int y = 0; y < 6; y++) {
            try {
                if (board.field[chipHeight][moveCmd - 3 + y] == drawingPlayer) {
                    winCondition++;
                    if (winCondition == 4) {
                        //System.out.println("lr");
                        endRound();
                    }
                } else {
                    winCondition = 0;
                }
            } catch (Exception e) {
                winCondition = 0;
            }
        }
        winCondition = 0;

        //Checking from bottom to top
        for (int y = 0; y < 6; y++) {
            try {
                if (board.field[chipHeight + 3 - y][moveCmd] == drawingPlayer) {
                    winCondition++;
                    if (winCondition == 4) {
                        //System.out.println("bt");
                        endRound();
                    }
                } else {
                    winCondition = 0;
                }
            } catch (Exception e) {
                winCondition = 0;
            }
        }

        winCondition = 0;

        //Checking from left bottom to top right
        for (int y = 0; y < 6; y++) {
            try {
                if (board.field[chipHeight + 3 - y][moveCmd - 3 + y] == drawingPlayer) {
                    winCondition++;
                    if (winCondition == 4) {
                        //System.out.println("lbtr");
                        endRound();
                    }
                } else {
                    winCondition = 0;
                }
            } catch (Exception e) {
                winCondition = 0;
            }
        }
        winCondition = 0;

        //Checking from right bottom to top left
        for (int y = 0; y < 6; y++) {
            try {
                if (board.field[chipHeight + 3 - y][moveCmd + 3 - y] == drawingPlayer) {
                    winCondition++;
                    if (winCondition == 4) {
                        //System.out.println("rbtl");
                        endRound();
                    }
                } else {
                    winCondition = 0;
                }
            } catch (Exception e) {
                winCondition = 0;
            }
        }

        //checking for PATT
        checkForPatt();

    }

    void checkForPatt() {
        //die äußerste if sollte man sich sparen können
        //if (running == true) {
        patt = true;
        for (int z = 0; z < board.boardSize.elementAt(1); z++) {
            if (board.field[0][z] == 0) {
                patt = false;
                break;
            }
        }
        if (patt == true) {
            //System.out.println("\n PATT");
            endRound();
        }
        //}
    }

    void endRound() {
        running = false;
    }

    boolean checkIfMovePossible(int moveCmd) {

        //Zeile existiert nicht
        if (moveCmd < 0 || moveCmd > board.boardSize.elementAt(1) - 1) {
            return false;
            //Zeile ist voll
        } else if (board.field[0][moveCmd] != 0) {
            return false;
        }
        return true;
    }

    String winnerIs() {
        if (drawingPlayer == 1) {
            return playerTwo.name;
        } else {
            return playerOne.name;
        }
    }

    void initBoard() {
        board = new Spielfeld() {

            @Override
            void displayBoard() {

                //numbers on top
                System.out.print("     ");
                for (int a = 0; a < boardSize.elementAt(1); a++) {

                    if (a < 10) {
                        System.out.print("0" + a + " ");
                    } else {
                        System.out.print(a + " ");
                    }
                }

                //borders top
                System.out.print("\n     ___");
                for (int a = 0; a < boardSize.elementAt(1) - 1; a++) {
                    System.out.print("___");
                }
                System.out.println();

                //display elements
                for (int x = 0; x < boardSize.elementAt(0); x++) {

                    if (x < 10) {
                        System.out.print("0" + x + ": [");
                    } else {
                        System.out.print(x + ": [");
                    }

                    for (int y = 0; y < boardSize.elementAt(1); y++) {
                        System.out.print(" " + field[x][y] + " ");
                    }
                    System.out.println("]");
                }

                //borders at the bottom
                System.out.print("     ¯¯¯");
                for (int a = 0; a < boardSize.elementAt(1) - 1; a++) {
                    System.out.print("¯¯¯");
                }
                System.out.println();
            }

            @Override
            void initField() {

                //[Tiefe][Breite]
                field = new int[boardSize.elementAt(0)][boardSize.elementAt(1)];

                for (int x = 0; x < boardSize.elementAt(0); x++) {
                    for (int y = 0; y < boardSize.elementAt(1); y++) {
                        field[x][y] = 0;
                    }
                }
            }
        };
    }

    void playerNmeDlg() {
        System.out.println("Welcome to VIERGWINNT.");
        System.out.println("Type in your name: ");

        while (playerOne.name == "") {
            try {
                playerOne.name = in.next();
            } catch (Exception e) {
                System.out.println("Wrong input. Enter a valid name!");
                in.nextLine();
            }
        }
        playerOne.type = true;
        System.out.println("Hello " + playerOne.name + ". Do you want to play " +
                "against a friend or against BMO?\n");
        System.out.println("Type 1 to play against a friend");
        System.out.println("Type some other number to play against a computer");

        //VS Human or BMO?
        int versus;

        while (true) {
            try {
                versus = in.nextInt();
                break;
            } catch (Exception e) {
                System.out.println("Wrong input. Try again!");
                in.nextLine();
            }
        }

        if (versus == 1) {
            playerTwo.type = true;
            System.out.println("Welcome Player Two. What is your name?");

            while (playerTwo.name == "") {
                try {
                    playerTwo.name = in.next();
                } catch (Exception e) {
                    System.out.println("Wrong input. Enter a valid name!");
                    in.nextLine();
                }
            }

            System.out.println("Hello " + playerTwo.name + ". Good luck!");
        } else {
            playerTwo.name = "BMO";
            System.out.println("Good luck BMO!");
        }
    }

    void setFldSize() {
        System.out.println("Set the board size: [4-32 Tiefe][4-32 Breite]");
        int x = 0;
        int y = 0;

        while (x > 32 || x < 4) {
            try {
                x = in.nextInt();
            } catch (Exception e) {
                System.out.println("Wrong input. Try again!");
                in.nextLine();
            }
            if (x > 32 || x < 4) System.out.println("Invalid field size");
        }
        while (y > 32 || y < 4) {
            try {
                y = in.nextInt();
            } catch (Exception e) {
                System.out.println("Wrong input or invalid field size. Try again!");
                in.nextLine();
            }
            if (y > 32 || y < 4) System.out.println("Invalid field size");
        }

        Vector size = new Vector();
        size.add(x);
        size.add(y);
        board.boardSize = size;

        System.out.println("The board size is: " + board.boardSize.toString() + "\n");
    }

    void printMoveHistory() {
        for (int[] x : moveHistory()
        ) {
            System.out.println(x[0] + ":" + x[1]);
        }
    }

    @Override
    public void logDraw(String moveCmd){}

    @Override
    public void playDraw(String moveCmd, int playerNumber){}

    //algorithm for intelligent computer opponent play
    //TODO: implement
    String bmoThinks(){
        return "moveCommand";
    }
}
