import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server {

    /**
     * Class Server
     *
     * Starts a Server, which listens for incoming connections
     * -> every time a client connects, a new Serverthread is initialized and put into the clientlist (add(...))
     *      -> every client gets a specific threadIndex = threadCounter with which you can find him
     * -> [!missing implementation!] every time a client disconnects, they are removed from the clientlist
     **/

    //Grundlage:    https://www.codejava.net/java-se/networking/java-socket-server-examples-tcp-ip

    //Helped:
    //              https://stackoverflow.com/questions/13115784/sending-a-message-to-all-clients-client-server-communication
    //              http://pirate.shu.edu/~wachsmut/Teaching/CSAS2214/Virtual/Lectures/chat-client-server.html

    //maybe there is another way to do it, than with a static clientList :)
            //-> in interface globale variable setzen wäre auch eine möglichkeit aber unschön und unnütz
            //-> singleton (abkürzung single skeleton)
    public static ArrayList<ServerThread> clientList;
    private Integer threadCounter = 0;

    public Server(){
        //TODO
        /*  TODO 1: Multithreading                                                                                          [x]
                    -> damit der Server auch alle Clienten auf einmal servern kann

            TODO 2: Socket-Listener... der es neuen Clients ermöglicht, sich anzumelden.                                    [x]
                    -> praktisch schon fertig (accept), aber kann noch verfeinert werden und ist später der Entry-Point
                    für die Intialisierung des Anmeldevorgangs

            TODO 3: Message-Listener... welcher die Voraussetzung für den Nachrichtenaustausch zwischen Clients schafft.    [x]
                    -> hier ist wichtig herauszufinden wie ich den Server an alle Clients Nachrichten schicken lasse,
                    sollte aber nicht weiter schwer sein

            TODO 4: (transiente?) Speicherung der Namen und Passwörter                                                      [x]

            TODO 5: Anmeldevorgang                                                                                          [x]
            TODO 6: Zusendung einer aktuellen Liste der Namen von anderen, bereits angemeldeten                             [x]
                    Clients zu dem sich gerade angemeldeten Client. Außerdem soll eine Meldung, dass
                    sich ein neuer Client angemeldet hat, an alle anderen bereits angemeldeten Clients gesendet
                    werden.

            TODO a: Maybe combine ClientThread and ServerThread to a "listenerThread", but meeeh :^)
        */

        //vielleicht zu einem Konsolenargument umschreiben
        int port = 6868;

        //initializing list for commecting clients
        clientList = new ArrayList<ServerThread>();

        try(ServerSocket serverSocket = new ServerSocket(port)){

            //server is up -> print
            System.out.println("Server is listening on port " + port);

            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("New client connected :^)!!");

                add(socket);
            }

        }catch(IOException ex){
            //logging the error
            System.out.println("Server Error: " + ex.getMessage());
            ex.printStackTrace();
        }
    }

    //initialize ServerThread (listening for - abd representing one client), and adding him to clientList
    public void add(Socket socket){
        //check for integer overflow <_>...!
        threadCounter++;
        ServerThread st = new ServerThread(socket, threadCounter);
        st.start();
        clientList.add(st);
    }

    //if client disconnects -> delete him from the clientList
    public void removeSocket(){
        //TODO: Implement :)! -> if one client disconnects, remove him from the list
    }

    public static void main(String[] args)  {
        new Server();
    }

}
