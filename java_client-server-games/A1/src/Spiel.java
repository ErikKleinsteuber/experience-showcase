import java.util.Scanner;

public abstract class Spiel {

    //Zustandsvariable für die Spieler.
    Spieler playerOne = new Spieler();
    Spieler playerTwo = new Spieler();

    //Zustandsvariable für das Spielfeld.
    Spielfeld board;

    //Definieren der abstrakten Methoden
    //für einen Spielzug und einen Durchgang.
    abstract void playDraw(int moveCmd, int playerNumber);
    abstract void playDraw(String moveCmd, int playerNumber);

    abstract void simulatePass();

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        System.out.println("Welcome. Choose a Game!");
        System.out.println("For VIERGEWINNT type: 1");
        System.out.println("For CHOMP type some other number");

        while (true) {
            try {
                if (in.nextInt() == 1) {
                    //Viergewinnt game = new Viergewinnt();
                    new Viergewinnt();
                    break;
                } else {
                    //TODO: implement second game
                    new Chomp();
                    break;
                }
            } catch (Exception e) {
                System.out.println("Wrong input. Try again!");
                in.nextLine();
            }
        }

    }


}
