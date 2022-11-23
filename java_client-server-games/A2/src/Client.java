import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client {

    public static void main(String[] args) {

        //TODO
        /*
        TODO s.Aufgabe: Möglichkeit zum Aufbau und Trennen einer Verbindung mit dem Server.
                        Möglichkeit zum Senden von Nachrichten an alle angemeldeten Clients.
                        Empfangen und Visualisieren von eingehenden Nachrichten.
         */

        String hostname = args[0];
        int port = Integer.parseInt(args[1]);

        try (Socket socket = new Socket(hostname, port)) {

            //start thread that listens for - and prints server messages
            Thread t = new Thread(new ClientThread(socket));
            t.start();

            OutputStream output = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(output, true);

            Console console = System.console();
            String text;

            do {
                //get user input
                text = console.readLine("");

                //write to Server
                writer.println(text);
            } while (!text.equals("bye"));

            //socket.close();                                                               //scheint unnoetig zu sein
        } catch (UnknownHostException e) {

            System.out.println("Server not found: " + e.getMessage());

        } catch (IOException e) {

            System.out.println("I/O error: " + e.getMessage());
        }
    }
}


