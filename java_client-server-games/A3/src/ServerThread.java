import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Map;

public class ServerThread extends Thread {

    private Socket socket;
    private InputStream input;
    private BufferedReader reader;
    private OutputStream output;
    private PrintWriter writer;
    private Integer threadIndex;
    private String userName;

    //TODO: maybe refactor all reader.readlines() to its own method -> so error handling can be done easier
    //TODO: rewrite the command sections
    //TODO: runningGamesList -> Server and the logic for that
    //TODO: delete invitations and runninggames from the lists if necessary

    public ServerThread(Socket socket, int threadIndex) {

        this.socket = socket;
        this.threadIndex = threadIndex;

        try {
            this.input = socket.getInputStream();
            this.reader = new BufferedReader(new InputStreamReader(input));

            this.output = socket.getOutputStream();
            this.writer = new PrintWriter(output, true);
        } catch (IOException ex) {
            System.out.println("Error in serverthread -> Constructor()!");
            Server.serverWindow.appendMessage("Error in Thread " + this.threadIndex + ex.getMessage(),"error");
            ex.printStackTrace();
        }
    }

    public void run() {
        try {
            loginBhvior();

            //variable to gather user input
            String text;

            //loop to gather input and if not null -> send to All other clients (without the client sending the msg)
            do {
                //TODO #1: hier ansetzen um mehrere Lines auf einmal lesen zu können
                //TODO #2: timeout for the reader
                //setting timeout for the reader -> https://stackoverflow.com/questions/6792835/how-do-you-set-a-timeout-on-bufferedreader-and-printwriter-in-java-1-4

                do{
                    text = reader.readLine();
                }while(text.equals(""));

                System.out.println("ClientMessage from user " + this.userName + ": " + text);

                text = checkForTextNull(text);

                String command = extractCommand(text);
                text = cropCommand(text, command);
                evaluateCommand(text, command);

            } while (!text.equals("/logout"));

            logOff();

            //disconnecting
            writeMessage("/system Good bye " + this.userName + " :)!");
            //Server.serverWindow.appendMessage("Good bye " + this.userName + " :)!", "system");
            this.logOff();
            socket.close();

        } catch (IOException ex) {
            //if Client breaks the connection via console interrupt, -> will throw a Connection reset error
            //maybe improve the error handling here even a little bit more -> can help with the multihread-testing
            System.out.println("Server exception: " + ex.getMessage());
            Server.serverWindow.appendMessage("Error in Thread " + this.threadIndex + ex.getMessage(),"error");
            ex.printStackTrace();

        }//if this error is catched -> ServerThread isn't killed at logoff state
        catch (NullPointerException ex){
            System.out.println("Server exception: " + ex.getMessage() + " [Empty message!]");
            Server.serverWindow.appendMessage("Error in Thread " + this.threadIndex + ex.getMessage() + "[Empty message!]","error");
            this.logOff();
        }
    }

    public String extractCommand(String text){
        String command = "";
        try{
            if(text.charAt(0) == '/'){
                for(char letter : text.toCharArray()){
                    if (letter == ' '){
                        break;
                    }
                    command += letter;
                }
            }
        }catch(StringIndexOutOfBoundsException oob){
            //handle error
            System.out.println("Failed at extracting command in ServerThread -> run(): \n" + "message: " + text + "\ncommand: " + command);
        }
        return command;
    }

    public String cropCommand(String text, String command){
        if(command.length() > 0 && text.length()>=command.length()+2){
            text = text.substring(command.length() + 1);
        }
        return text;
    }

    public void evaluateCommand(String text, String command){

        switch (command){
                //whispering
            case "/w":
                whisper(text);
                break;

                //invitations
            case "/invite":
                invite(text);
                break;

                //accept of invitation
            case "/yes":
                acceptInvite(text);
                break;

                //drawing in a game
            case "/draw":
                //System.out.println("/draw " + text);
                for(ArrayList<String> game : Server.runningGamesList){
                    System.out.println(game.get(0) + game.get(1));
                    if(game.get(0).equals(this.userName)){
                        sendToOne(command, text, game.get(1),"");
                        break;
                    }else if(game.get(1).equals(this.userName)){
                        sendToOne(command, text, game.get(0),"");
                        break;
                    }
                    //System.out.println("You can't draw if you are not playing");
                }
                break;

                //surrendered a game
            case "/surrender":
                for(ArrayList<String> game : Server.runningGamesList){
                    //System.out.println(game.get(0) + game.get(1));
                    if(game.get(0).equals(this.userName)){
                        sendToOne(command, "", game.get(1),"");
                        break;
                    }else if(game.get(1).equals(this.userName)){
                        sendToOne(command, "", game.get(0),"");
                        break;
                    }
                    //System.out.println("You can't draw if you are not playing");
                }
                break;

                //finished a game
            case "/end":
                for(int x = 0; x<Server.runningGamesList.size(); x++){
                    if(Server.runningGamesList.get(x).get(0).equals(this.userName)
                            || Server.runningGamesList.get(x).get(1).equals(this.userName)) {
                        Server.serverWindow.appendMessage("Game of " + Server.runningGamesList.get(x).get(2) +
                                " -> " + Server.runningGamesList.get(x).get(0) + " vs " + Server.runningGamesList.get(x).get(1) +
                                "has ended", "system");
                        Server.runningGamesList.remove(x);
                        Server.serverWindow.refreshGamesList(Server.runningGamesList);
                        break;
                    }
                }
                break;

                //no or false command
            default:
                if(!command.equals("")){
                    writeMessage("Your command '" + command + "' does not exist. Type /help for a list of possible commands.");
                }else{
                    sendToAll("/user",this.userName + ": ", text);
                    Server.serverWindow.appendMessage(this.userName + ": " + text, "user");
                }
        }

    }

    public String extractName(String text){
        String name = "";

        try{
            for(char letter : text.toCharArray()){
                if (letter == ' '){
                    break;
                }
                name += letter;
            }
        }catch(StringIndexOutOfBoundsException oob){
            //handle error
            System.out.println("Failed at extracting name in ServerThread -> run(): \n" + "message: " + text + "\nname: " + name);
        }
        return name;
    }

    public void whisper(String text){
        String name = "";
        for(char letter : text.toCharArray()){
            if (letter == ' '){
                break;
            }
            name += letter;
        }
        if(checkIfUserOnline(name)){
            try{
                text = text.substring(name.length() + 1);
                writeMessage("/w " + "To " + name + ": " + text);
                sendToOne("/w",this.userName + ": ",name,text);
                Server.serverWindow.appendMessage(this.userName + " whispers to " + name + ": " + text, "user");
            }catch (StringIndexOutOfBoundsException sOob){
                //message was empty
            }
        }else{
            writeMessage("User " + name + " does not exist or is not online at the moment.");
        }
    }

    public void invite(String text){

        String name = "";
        name = extractName(text);
        if(!name.equals(this.userName)){
            if(checkIfUserOnline(name)){
                try{
                    text = text.substring(name.length() + 1);
                    boolean pendingInvites = false;

                    try{
                        for(ArrayList<String> invites : Server.invitationsList){
                            if(invites.get(0).equals(this.userName)){
                                pendingInvites = true;
                            }
                        }
                    }catch (ArrayIndexOutOfBoundsException aaobex){
                        //handle error
                        System.out.println("no invites yet.");
                    }

                    if(text.equals("1")){
                        //TODO: only one invite at once allowed
                        //TODO: only one invitation accept at once allowed
                        //TODO: if you're in game you can not invite or accept
                        //TODO: implement accept and other importent things concerning the invitation thing
                        //TODO: implement /yes , /help and /clearinvites comments
                        //System.out.println(this.userName + " invited " + name);

                        if(pendingInvites){
                            writeMessage("You already have a pending invite. Type /clearinvites to delete it.");
                        }else{
                            ArrayList<String> invite = new ArrayList<>();
                            invite.add(this.userName);
                            invite.add(name);
                            invite.add(text);
                            Server.invitationsList.add(invite);
                            Server.serverWindow.refreshInvitationsList(Server.invitationsList);

                            writeMessage("/w " + "To " + name + ": " + "Invitation to Futtern.");
                            sendToOne("/w",this.userName + ": ",name,"Invited you to play a game of 1. Write /yes " + this.userName + " to accept.");
                            Server.serverWindow.appendMessage(this.userName + " invited " + name + " to a game of 1", "user");
                        }

                    }else if(text.equals("2")){
                        if(pendingInvites){
                            writeMessage("You already have a pending invite. Type /clearinvites to delete it.");
                        }else{
                            ArrayList<String> invite = new ArrayList<>();
                            invite.add(this.userName);
                            invite.add(name);
                            invite.add(text);
                            Server.invitationsList.add(invite);
                            Server.serverWindow.refreshInvitationsList(Server.invitationsList);

                            writeMessage("/w " + "To " + name + ": " + "Invitation to 4-Gewinnt.");
                            sendToOne("/w",this.userName + ": ",name,"Invited you to play a game of 2. Write /yes " + this.userName + " to accept.");
                            Server.serverWindow.appendMessage(this.userName + " invited " + name + " to a game of 2", "user");
                        }
                    }else{
                        writeMessage("Invalid command format. Invite via: '/invite username 1' for a game of 4 gewinnt or '... 2' for a game of 2.");
                    }
                }catch (StringIndexOutOfBoundsException sOob){
                    //message was empty
                    writeMessage("Invalid command format. Invite via: '/invite username 1' for a game of 4 gewinnt or '... 2' for a game of 2.");
                }
            }else{
                writeMessage("User " + name + " does not exist or is not online at the moment.");
            }
        }else{
            writeMessage("You can't invite yourself.");
        }

    }

    public void removeInvite(){
        for(int x = 0;x<Server.invitationsList.size();x++){
            if(Server.invitationsList.get(x).get(0).equals(this.userName)
                    ||Server.invitationsList.get(x).get(1).equals(this.userName)){
                        Server.invitationsList.remove(x);
                        Server.serverWindow.refreshInvitationsList(Server.invitationsList);
            }
        }
    }

    public void acceptInvite(String text){
        String name = "";
        name = extractName(text);

        boolean inviteExists = false;
        boolean ingame = false;
        String gameNumber = "";

        try{
            for(ArrayList<String> games : Server.runningGamesList){
                if(games.get(0).equals(this.userName) || games.get(1).equals(this.userName)){
                    //TODO: user is already in game
                    ingame = true;
                    break;
                }
            }
        }catch (ArrayIndexOutOfBoundsException aoob){
            //handle Error
        }

        try{
            for(ArrayList<String> invites : Server.invitationsList){
                if(invites.get(1).equals(this.userName) && invites.get(0).equals(name)){
                    gameNumber = invites.get(2);
                    inviteExists = true;
                    break;
                }
            }
        }catch (ArrayIndexOutOfBoundsException aaobex){
            //handle error
            System.out.println("no invites yet.");
        }

        System.out.println(this.userName + " invit = " + inviteExists + " " + ingame);

        if(inviteExists){
            if(!ingame){
                //TODO: start game here
                //System.out.println("Invitation accept successful, starting game now.");
                ArrayList<String> game = new ArrayList<>();
                game.add(name);
                game.add(this.userName);
                game.add(gameNumber);
                Server.runningGamesList.add(game);
                Server.serverWindow.refreshGamesList(Server.runningGamesList);
                String number = "";
                for(ArrayList<String> inv : Server.invitationsList){
                    if (inv.get(0).equals(name) && inv.get(1).equals(this.userName)){
                        number = inv.get(2);
                        //System.out.println("The game is " + number);
                        break;
                    }
                }
                removeInvite();
                Server.serverWindow.appendMessage("Starting a game of " + gameNumber + " " + this.userName + " vs " + name, "system");
                sendToOne("/start", "", this.userName, number + " " + name + " " + this.userName + " 2");
                sendToOne("/start", "", name, number + " " + this.userName + " " + name + " 1");
                //TODO: remove invites! pretty hard task..
            }else{
                writeMessage("You can't accept an invitation if you are already in a game.");
            }
        }else{
            writeMessage("The invitation you responded to does not exist anymore.");
        }
    }

    public String checkForTextNull(String text){
        //if client writes "/logout" or "null" or presses strg+c in console -> his application and thread will close
        //TODO: rewrite or delete this part -> cant strg+c in a chatwindow
        if(text == null || text.equals(null) || text.equals("null")){
            text = "/logout";
        }
        return text;
    }

    //irgendwie anders machen als durch parameter, -> reader und writer eventuell einfach global >-<?!
    public synchronized void loginBhvior() {
        dataManager dm = new dataManager();
        String userName = "";
        String password = "";
        //TODO: userName darf keine Leerzeichen o.Ä. enthalten
        do {
            try {
                boolean userNotOnline;
                boolean userFound;
                do {
                    writer.println("/system Enter username: ");
                    userName = reader.readLine();
                    if (checkIfUserOnline(userName)) {
                        writer.println("/system User with userName " + userName + " is already online.");
                        userNotOnline = false;
                    } else {
                        userNotOnline = true;
                    }
                    if (!dm.checkIfUserExists(userName)) {
                        writer.println("/system There is no user with the name " + userName);
                        writer.println("/system Wanna create a new Account? -> type in yes");
                        userFound = false;
                        if (reader.readLine().equals("yes")) {
                            //create new account
                            writer.println("/system Choose password: ");
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

                writer.println("/system Enter password: ");
                password = reader.readLine();
            } catch (IOException ex) {
                writer.println("/error " + ex.getMessage());
                Server.serverWindow.appendMessage("Error in Thread " + this.threadIndex + ex.getMessage(), "error");
                ex.printStackTrace();
            }
        } while (!dm.checkAcces(userName, password) || userName == "" || password == "");

        //setting userName for the Thread
        this.userName = userName;

        //hier wird die Liste aktualisiert in der Serverkonsole
        //Server.serverWindow.appendUser(userName);

        Server.serverWindow.refreshUserList(getAllUsers());
        sendToAll("/updateCL", "",  getAllUsersToString());

        writer.println("/system Successfully logged in :)! Welcome to the Server " + this.userName + ".");
        Server.serverWindow.appendMessage("Successfully logged in :)! Welcome to the Server " + this.userName + ".", "system");

        sendToAll("/system", this.userName, " <- has just joined the Server :D! What a thrill.");
    }

    public void writeMessage(String message) {
        writer.println(message);
    }

    public void sendToAll(String type, String prefix, String message) {
        //special case -> strg + c

        if(message == null){
            System.out.println("NULL OBJEKT Message -> Assuming Ctrl+C Console input command. Shutting down socket.");
            return;
        }

        if (message.equals(null) || message.equals("") || message.equals("/logout")) {
            return;
        }

        for (ServerThread x : Server.clientList) {
            //auskommentiert damit auch der Sender die Nachricht erhält
            //einkommentieren und der Sender erhält seine eigene Nachricht nichtmehr
            if (/*x.threadIndex != this.threadIndex && */x.userName != null) {
                //x.writeMessage(user + ": " + message);
                x.writeMessage(type + " " + prefix + message);
            }
        }
    }

    public void sendToOne(String type, String prefix, String name, String message){
        for (ServerThread x : Server.clientList) {
            if (/*x.threadIndex != this.threadIndex && */x.userName.equals(name)) {
                //x.writeMessage(user + ": " + message);
                x.writeMessage(type + " " + prefix + message);
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

    public ArrayList<String> getAllUsers(){
        ArrayList<String> allUsers = new ArrayList<>();

        for (ServerThread x : Server.clientList) {
            if(x.userName != null){
                allUsers.add(x.userName);
            }
        }

        return allUsers;
    }

    public String getAllUsersToString(){
        String allUsers = "";
        for (ServerThread x : Server.clientList) {
            if(x.userName != null){
                allUsers += x.userName + " ";
            }
        }

        return allUsers;
    }

    public boolean checkIfUserOnline(String username) {
        for (ServerThread x : Server.clientList) {
            try {
                if (x.userName.equals(username)) {
                    return true;
                }
            } catch (NullPointerException ex) {

                //when many people are logging in, this error gets printed a lot!
                //System.out.println("Server exception: " + ex.getMessage() + "[Either nobody is online or somebody " +
                //        "is logging in right now.]");

                //not important to print
                //ex.printStackTrace();

                //if nullpointer -> either no users online -> return true, or username of the current looked at
                //thread is not set yet -> look for other client names
            }
        }
        return false;
    }

    public void logOff(){
        for (ServerThread x : Server.clientList){
            if (this.threadIndex == x.threadIndex){
                //System.out.println("Logging out user: " + x.userName + " with threadIndex: " + x.threadIndex);
                Server.serverWindow.appendMessage("Logging out user: " + x.userName + " with threadIndex: " + x.threadIndex, "system");
                Server.clientList.remove(x);
                Server.serverWindow.refreshUserList(getAllUsers());
                sendToAll("/updateCL", "",  getAllUsersToString());
                break;
            }
        }
    }
}
