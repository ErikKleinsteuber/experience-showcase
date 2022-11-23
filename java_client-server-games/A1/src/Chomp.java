import java.util.LinkedList;
import java.util.Scanner;
import java.util.Vector;
import java.util.concurrent.ThreadLocalRandom;

public class Chomp extends Spiel implements Protokolierbar {

    Scanner in = new Scanner(System.in);

    boolean running, wannaPlay;
    private LinkedList<int[]> moveHistory = new LinkedList<>();

    int drawingPlayer = 1;      //which players draw it is
    String moveCmd = "";        //moveCommand for passing the moves

    public Chomp() {

        //SETUP BEGIN
        initBoard();

        //Player name dialogue
        playerNmeDlg();

        //Set Field Size
        setFldSize();

        board.initField();

        System.out.println("Let the games begin!\n");
        System.out.println("Player 1: " + playerOne.name + " VS Player 2: " + playerTwo.name);
        //SETUP END

        //ENTRY POINT
        gameLoop();
    }

    void gameLoop() {
        running = true;         //if round is running
        wannaPlay = true;       //checks if User wants to play another round

        board.initField();      //setup-/clear board
        board.displayBoard();

        //GAME LOOP
        while (wannaPlay == true) {             //starts new games while Player wants to play (without changing setup)
            while (running == true) {           //simulates passes while game is running
                simulatePass();                 //simulates pass (player 1 draws and then player 2)
            }
            System.out.println("GAME OVER.");

            System.out.println("WINNER IS " + winnerIs());

            moveHistory().clear();              //clear history for a fresh new game
            System.out.println("Wanna play again? [y=1/n=else]?");
            try {
                if (in.nextInt() == 1) {
                    gameLoop();
                } else {
                    wannaPlay = false;
                }
            } catch (Exception e) {
                System.out.println("Wrong input. Closing Chomp now, good-bye :)");
                wannaPlay = false;
            }
        }

    }

    @Override
    public LinkedList<int[]> moveHistory() {
        return moveHistory;
    }

    @Override
    public void logDraw(int moveCmd) {}

    @Override
    public void logDraw(String moveCmd){
        try{
            int[] moveLog = new int[3];
            moveLog[0] = drawingPlayer;
            moveLog[1] = Integer.parseInt(moveCmd.substring(1,2));
            moveLog[2] = Integer.parseInt(moveCmd.substring(3,4));
            moveHistory().add(moveLog);
        }catch(Exception e){
            System.out.println(e);
        }
    }

    @Override
    public void undoDraw() {
        moveHistory().pollLast();

        board.initField();
        for (int[] x : moveHistory()
        ) {
            String moveString = Integer.toString(x[1] * 100 + x[2]);

            while(moveString.length() != 4)
            {
                moveString = "0" + moveString;
            }

            playDraw(moveString,x[0]);
        }
    }

    @Override
    void playDraw(String moveCmd, int playerNumber) {
        int height = Integer.parseInt(moveCmd.substring(1,2));
        int width = Integer.parseInt(moveCmd.substring(3,4));

        for (int x = height; x < board.boardSize.elementAt(0); x++) {
            for (int y = width; y < board.boardSize.elementAt(1); y++) {
                if (board.field[x][y] == 0){
                    board.field[x][y] = playerNumber;
                }
            }
        }

    }

    @Override
    void playDraw(int moveCmd, int playerNumber) {}

    @Override
    void simulatePass() {

        moveCmd = "";           //resetting moveCommand
        boolean undo = false;   //if player wants to undo last draw

        //"Durchgang" roundloop (player 1 -> player 2)
        for (int x = 0; x < 2; x++) {

            //break if game over
            if (running == false) break;

            //Computer moves
            if (drawingPlayer == 2 && playerTwo.type == false) {

                String[] pMoves = getPossibleMoves();
                //TODO: implement Computer drawing
                //System.out.println("BMO draws...");
                int rng = ThreadLocalRandom.current().nextInt(0, pMoves.length-1);

                try{
                    moveCmd = pMoves[rng];
                    System.out.println("MOVE = " + pMoves[rng]);
                }catch(Exception e){
                    System.out.println(e);
                }
                //System.out.println(rng + " " + getPossibleMoves()[rng]);
                //TODO: new rng for chomp needed
            }else {

                //humans move
                while (checkIfMovePossible(moveCmd) == false) {
                    System.out.println("Make a move Player " + drawingPlayer);

                    try {
                        moveCmd = in.next();
                    } catch (Exception e) {
                        in.nextLine();
                    }

                    //removing draw
                    if (Integer.parseInt(moveCmd) < 0) {
                        undo = true;
                        break;
                    }

                    if (checkIfMovePossible(moveCmd) == false) System.out.println("Incorrect moveCommand. Try again!");
                }
            }

            if (undo == true) {             //undo
                undoDraw();
                moveCmd = "";
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
                validateGame();
            }

            //turn logic
            //-> flips drawing player and counts up the loop
            if (drawingPlayer == 1) {
                drawingPlayer = 2;
                x = 1;
            } else {
                drawingPlayer = 1;
                x = 2;
            }

            //printMoveHistory();

            moveCmd = "";           //resetting moveCommand, just for the safety
        }
    }

    boolean checkIfMovePossible(String moveCmd){

        //check if input can be parsed to Integer
        try{
            Integer.parseInt(moveCmd);
        }catch(Exception e){
            return false;
        }

        //check if it matches the board/field-size
        try{
            if (Integer.parseInt(moveCmd.substring(1,2)) > board.boardSize.elementAt(0) - 1 ||
                    Integer.parseInt(moveCmd.substring(3,4)) > board.boardSize.elementAt(1) - 1 ||
                    Integer.parseInt(moveCmd.substring(1,2)) < 0 ||
                    Integer.parseInt(moveCmd.substring(3,4)) < 0)
            {
                return false;
            }
        }catch(Exception e){
            return false;
        }

        //check if the input is not exactly 4 long (format reasons) || if the field is not free
        if (moveCmd.length() != 4 ||
                board.field[Integer.parseInt(moveCmd.substring(1,2))]
                        [Integer.parseInt(moveCmd.substring(3,4))] != 0
        )
        {
            return false;
        }else{              // -> valid move, well done
            return true;
        }
    }

    String[] getPossibleMoves(){

        String[] pmoves = new String[board.boardSize.elementAt(0) * board.boardSize.elementAt(1)];
        int counter = 0;
        for (int x = 0; x < board.boardSize.elementAt(0); x++) {
            for (int y = 0; y < board.boardSize.elementAt(1); y++) {
                if (board.field[x][y] == 0){
                    String moveString = Integer.toString(x*100 + y);
                    while(moveString.length() != 4)
                    {
                        moveString = "0" + moveString;
                    }
                    pmoves[counter] = moveString;
                    counter++;
                }
            }
        }

        return pmoves;
    }

    //checks for game over and quits round if game over -> breaking the game loop
    void validateGame(){
        if (getPossibleMoves().length == 0){
            running = false;
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
                //inits board with zeroes
                //[height][width]
                field = new int[boardSize.elementAt(0)][boardSize.elementAt(1)];

                for (int x = 0; x < boardSize.elementAt(0); x++) {
                    for (int y = 0; y < boardSize.elementAt(1); y++) {
                        field[x][y] = 0;
                    }
                }
                field[0][0] = 3;
            }
        };
    }

    void playerNmeDlg() {
        System.out.println("Welcome to CHOMP.");
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
                System.out.println("Wrong input. Try again! 1");
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
        System.out.println("Set the board size: [3-32 height][6-32 width]");
        int x = 0;
        int y = 0;

        while (x > 32 || x < 3) {
            try {
                x = in.nextInt();
            } catch (Exception e) {
                System.out.println(e);
                //System.out.println("Wrong input. Try again!");
                in.nextLine();
            }
            if (x > 32 || x < 3) System.out.println("Invalid field size");
        }
        while (y > 32 || y < 6) {
            try {
                y = in.nextInt();
            } catch (Exception e) {
                System.out.println(e);
                //System.out.println("Wrong input. Try again!");
                in.nextLine();
            }
            if (y > 32 || y < 6) System.out.println("Invalid field size");
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
            System.out.println(x[0] + ":" + x[1] + ":" + x[2]);
        }
    }

    //returns name of the Player who has won
    String winnerIs(){
        if (drawingPlayer == 1){
            return playerTwo.name;
        }else{
            return playerOne.name;
        }
    }

    //algorithm for intelligent computer opponent play
    //TODO: implement
    String bmoThinks(){
        return "moveCommand";
    }
}
