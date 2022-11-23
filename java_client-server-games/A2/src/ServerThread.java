import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class ServerThread extends Thread {

    private Socket socket;
    private InputStream input;
    private BufferedReader reader;
    private OutputStream output;
    private PrintWriter writer;
    private Integer threadIndex;
    private String userName;

    //TODO: refactor all reader.readlines() to its own method -> so error handling can be done easier

    public ServerThread(Socket socket, int threadIndex) {

        this.socket = socket;
        this.threadIndex = threadIndex;

        try {
            this.input = socket.getInputStream();
            this.reader = new BufferedReader(new InputStreamReader(input));

            this.output = socket.getOutputStream();
            this.writer = new PrintWriter(output, true);
        } catch (IOException ex) {
            System.out.println("Error in serverthread constructor!");
            writer.println("Server exception: " + ex.getMessage());
            ex.printStackTrace();
        }
    }

    public void run() {
        try {

            //client connects -> start the loginbehaviour
            loginBhvior();

            //variable to gather user input
            String text;

            //loop to gather input and if not null -> send to All other clients (without the client sending the msg)
            do {
                //setting timeout for the reader -> https://stackoverflow.com/questions/6792835/how-do-you-set-a-timeout-on-bufferedreader-and-printwriter-in-java-1-4
                //bcs if Client just crashes, Server thinks that Client is logged in forever (until Server shoutdown)
                text = reader.readLine();

                //check for null
                sendToAll(this.userName, text);

            } while (!text.equals("bye"));

            //disconnecting

            //server-sided good bye (does not reach its client if it closes its socket automatically
            //      -> so i wrote another client-sided good bye >o<
            writeMessage("Good bye " + this.userName + " :)!");

            this.logOff();
            socket.close();
        } catch (IOException ex) {
            //if Client breaks the connection via console interrupt, -> will throw a Connection reset error
            //maybe improve the error handling here even a little bit more -> can help with the multihread-testing
            System.out.println("Server exception: " + ex.getMessage());
            ex.printStackTrace();

        }//if this error is catched -> ServerThread isn't killed at logoff state
        catch (NullPointerException ex){
            System.out.println("Server exception: " + ex.getMessage() + " [Empty message!]");
            this.logOff();
        }
    }

    //irgendwie anders machen als durch parameter, -> reader und writer eventuell einfach global >-<?!
    public synchronized void loginBhvior() {
        dataManager dm = new dataManager();
        String userName = "";
        String password = "";
        do {
            try {
                boolean userNotOnline;
                boolean userFound;
                do {
                    writer.println("Enter username: ");
                    userName = reader.readLine();
                    if (!checkIfuserNotOnline(userName)) {
                        writer.println("User with userName " + userName + " is already online.");
                        userNotOnline = false;
                    } else {
                        userNotOnline = true;
                    }
                    if (!dm.checkIfUserExists(userName)) {
                        writer.println("There is no user with the name " + userName);
                        writer.println("Wanna create a new Account? -> type in yes");
                        userFound = false;
                        if (reader.readLine().equals("yes")) {
                            //create new account
                            writer.println("Choose password: ");
                            do {
                                password = reader.readLine();
                                //TODO: if password is empty, tell the user!
                            } while (password.equals("") || password == null);
                            if (dm.createAccount(userName, password)) {
                                userFound = true;
                            } else {
                                userFound = false;
                            }
                        }
                    } else {
                        userFound = true;
                    }
                } while (!userNotOnline || !userFound);

                writer.println("Enter password: ");
                password = reader.readLine();
            } catch (IOException ex) {
                writer.println("Server exception: " + ex.getMessage());
                ex.printStackTrace();
            }
        } while (!dm.checkAcces(userName, password) || userName == "" || password == "");

        //setting userName for the Thread
        this.userName = userName;

        writer.println("Successfully logged in :)! Welcome to the Server " + this.userName + ".");

        sendToAll(this.userName, " <- has just joined the Server :D! What a thrill.");
        writeMessage("Here is a list of all other active users: " + getAllOtherUsers().toString());
    }

    public void writeMessage(String message) {
        writer.println(message);
    }

    public void sendToAll(String user, String message) {
        //check if user is logged in!!!
        //handle potential errors

        //special case -> strg + c

        if(message == null){
            System.out.println("NULL OBJEKT Message -> Assuming Ctrl+C Console input command. Shutting down socket.");
            return;
        }

        if (message.equals(null) || message.equals("") || message.equals("bye")) {
            return;
        }

        for (ServerThread x : Server.clientList) {
            if (x.threadIndex != this.threadIndex && x.userName != null) {
                x.writeMessage(user + ": " + message);
            }
        }
    }

    public ArrayList<String> getAllOtherUsers() {
        ArrayList<String> allOtherUsers = new ArrayList<>();

        for (ServerThread x : Server.clientList) {
            if (x.userName != this.userName && x.userName != null) {
                allOtherUsers.add(x.userName);
            }
        }

        return allOtherUsers;
    }

    public boolean checkIfuserNotOnline(String username) {
        for (ServerThread x : Server.clientList) {
            try {
                if (x.userName.equals(username)) {
                    return false;
                }
            } catch (NullPointerException ex) {

                //when many people are logging in, this error gets printed a lot!
                System.out.println("Server exception: " + ex.getMessage() + "[Either nobody is online or somebody " +
                        "is logging in right now.]");

                //not important to print
                //ex.printStackTrace();

                //if nullpointer -> either no users online -> return true, or username of the current looked at
                //thread is not set yet -> look for other client names
            }
        }
        return true;
    }

    public void logOff(){
        for (ServerThread x : Server.clientList){
            if (this.threadIndex == x.threadIndex){
                System.out.println("Logging out user: " + x.userName + " with threadIndex: " + x.threadIndex);
                Server.clientList.remove(x);
                break;
            }
        }
    }
}
