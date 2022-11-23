import java.util.Vector;

public abstract class Spielfeld {
    Vector<Integer> boardSize;
    int[][] field;
    abstract void displayBoard();
    abstract void initField();
}
