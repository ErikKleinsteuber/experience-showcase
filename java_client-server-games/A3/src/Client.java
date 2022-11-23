import javax.swing.*;
import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;

public class Client {

    public static ClientWindow clientWindow;
    public static ClientGame1 game1;
    public static ClientGame2 game2;
    private static PrintWriter writer;

    //TODO: Anwendung beendet sich noch nicht richtig wenn der user sich ausloggt
    //      logout button und andere Quality of life improvements

    public static void main(String[] args) {

        //maybe put that in the ClientWindow as well
        Thread windowThread = new Thread(){
            public void run(){
                clientWindow = new ClientWindow();
                clientWindow.createFrame(clientWindow);
            }
        };

        windowThread.run();

        String hostname = args[0];
        int port = Integer.parseInt(args[1]);

        //TODO: [zum Schluss] rewrite that whole part -> input and output is already handled in ClientWindow and ClientThread
        try (Socket socket = new Socket(hostname, port)) {
            //start thread that listens for - and prints server messages

            OutputStream output = socket.getOutputStream();
            writer = new PrintWriter(output, true);

            Thread t = new Thread(new ClientThread(socket,output,writer));
            t.start();

            clientWindow.setOutStream(output, writer);

            Console console = System.console();
            String text;

            do {
                /**
                 * console does not read text anymore because this is handled by the window since task A3
                 * this loop here just waits, comment the write back in to make it function again but atm it is
                 * commented out for error reduction and to have only one possible source of input
                 * **/
                text = console.readLine("");

                //write to Server
                //writer.println(text);
            } while (!text.equals("bye"));
            socket.close();
        } catch (UnknownHostException e) {

            System.out.println("Server not found: " + e.getMessage());

        } catch (IOException e) {

            System.out.println("I/O error: " + e.getMessage());
        }
    }
}


