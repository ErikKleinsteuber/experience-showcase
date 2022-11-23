import java.util.*;


public interface Protokolierbar {

    //Zustandsvariable zum Protokollieren der Züge
    LinkedList<int[]> moveHistory();

    //Definieren einer abstrakten Methode zum Hinzufügen eines SpielzugesMit den
    //Parametern der Signatur soll ein Spielzug eindeutig identifiziert werden. Da nur Brettspiele
    //implementiert werden, bieten sich die Koordinaten sowie der Spieler zur Kennzeichnung
    //des Spielzuges an.
    void logDraw(int moveCmd);
    void logDraw(String moveCmd);

    //Definieren einer abstrakten Methode zum Entfernen eines Spielzuges.
    void undoDraw();
}
