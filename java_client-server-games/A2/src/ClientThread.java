import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;

public class ClientThread implements Runnable {

    private Socket socket;

    public ClientThread(Socket socket) {
        System.out.println("New ClientThread initialized. ");
        this.socket = socket;
    }

    @Override
    public void run() {
        System.out.println("Client thread is running :)");
        try {
            InputStream input = socket.getInputStream();                                //setting up input stream
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));   //wrapping it to a reader

            String serverMessage;

            do {
                //read message from the Server
                serverMessage = reader.readLine();

                //print it to Clients console
                System.out.println(serverMessage);
            } while (!serverMessage.equals("bye"));

            //is never reached, because when typing in bye -> at first the Clients Socket dies and then this method
            //catches an IOException -> jumps to catch block
            System.out.println("Good bye :)!");

            socket.close();
        }catch(IOException ex){
            //gets called when user types in bye -> not sure why though, maybe because Clients Socket died
            System.out.println("Server exception: " + ex.getMessage());

            if(ex.getMessage().equals("Socket closed")){
                System.out.println("Good Bye :)");
            }

            //not important to print that
            //ex.printStackTrace();
        }
    }
}
