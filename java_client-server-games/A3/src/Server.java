import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Server {

    /**
     * Class Server
     *
     * Starts a Server, which listens for incoming connections
     * -> every time a client connects, a new Serverthread is initialized and put into the clientlist (add(...))
     *      -> every client gets a specific threadIndex = threadCounter with which you can find him
     **/

    //TODO:     ping user every now and then to check if they are still connected
    //TODO:     container for going invitations and going games
    //TODO:     remake logout behaviour
    //TODO:     remake login behaviour

    //Grundlage:    https://www.codejava.net/java-se/networking/java-socket-server-examples-tcp-ip

    //Helped:
    //              https://stackoverflow.com/questions/13115784/sending-a-message-to-all-clients-client-server-communication
    //              http://pirate.shu.edu/~wachsmut/Teaching/CSAS2214/Virtual/Lectures/chat-client-server.html

    public static ArrayList<ServerThread> clientList;
    public static ServerWindow serverWindow = new ServerWindow();
    public static ServerSocket serverSocket;
    public static ArrayList<ArrayList<String>> invitationsList;
    public static ArrayList<ArrayList<String>> runningGamesList;
    private Integer threadCounter = 0;
    int port = 6868;

    public Server(){
        //TODO A3:
        //      serverSocket nicht static lassen, aber für nen gutes closing erstmal ein guter workaround
        //      Vielleicht noch eine Admin Chatzeile hinzufügen
        //      alles schön machen :*

        clientList = new ArrayList<ServerThread>();
        invitationsList = new ArrayList<ArrayList<String>>();
        runningGamesList = new ArrayList<ArrayList<String>>();

        try/*(ServerSocket serverSocket = new ServerSocket(port))*/{
            serverSocket = new ServerSocket(port);

            System.out.println("Server is listening on port " + port);

            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("New client connecting...");
                serverWindow.appendMessage("New client connecting...", "system");

                add(socket);
            }

        }catch(IOException ex){
            System.out.println("Server Error: " + ex.getMessage());
            serverWindow.appendMessage("Server Error: " + ex.getMessage(), "error");
            ex.printStackTrace();
        }
    }

    //initialize ServerThread (listening for - abd representing one client), and adding him to clientList
    public void add(Socket socket){
        //TODO: somehow make this safer or rewrite it
        threadCounter++;
        ServerThread st = new ServerThread(socket, threadCounter);
        st.start();
        clientList.add(st);
    }

    public static void main(String[] args)  {
        Thread windowThread = new Thread(){
            public void run(){
                serverWindow = new ServerWindow();
                serverWindow.createServerWindow(serverWindow);
            }
        };

        windowThread.run();

        new Server();
    }

}
