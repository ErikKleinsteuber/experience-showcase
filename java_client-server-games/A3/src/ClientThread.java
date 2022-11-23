import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class ClientThread implements Runnable {

    private Socket socket;
    OutputStream output;
    PrintWriter writer;
    static int currentRunningGame = 0;

    public ClientThread(Socket socket, OutputStream output, PrintWriter writer) {
        this.socket = socket;
        this.output = output;
        this.writer = writer;
    }

    @Override
    public void run() {
        System.out.println("Client thread is running :).");
        try {
            InputStream input = socket.getInputStream();                                //setting up input stream
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));   //wrapping it to a reader

            String serverMessage;

            System.out.println("Successfully created InputStream and Reader. You are now able to send to- and" +
                    "reveive messages from the Server.");

            do {
                //read message from the Server
                serverMessage = reader.readLine();

                System.out.println("Servermessage: " + serverMessage);

                String command = extractCommand(serverMessage);

                //crop command
                if(command.length() > 0){
                    serverMessage = serverMessage.substring(command.length() + 1);
                }

                //System.out.println("cmd = " + command + " msg = " + serverMessage);

                evaluateCommand(serverMessage,command);

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
        }catch(NullPointerException nPex){
            System.out.println("NullPointerException: " + nPex);
        }catch(StringIndexOutOfBoundsException sOob){
            sOob.printStackTrace();
            System.out.println("Cropping might have failed");
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

    public String extractCommand(String serverMessage){
        String command = "";
        try{
            if(serverMessage.charAt(0) == '/'){
                for(char letter : serverMessage.toCharArray()){
                    if (letter == ' '){
                        break;
                    }
                    command += letter;
                }
            }
        }catch(Exception ex){
            //handle error
        }
        return command;
    }

    public void evaluateCommand(String serverMessage, String command){

        switch (command){
                //einfache user-Message
            case "/user":
                Client.clientWindow.appendMessage(serverMessage,"user");
                break;

                //system-Message
            case "/system":
                Client.clientWindow.appendMessage(serverMessage,"system");
                break;

                //error-Message
            case "/error":
                Client.clientWindow.appendMessage(serverMessage,"error");
                break;

                //updatet die ClientList
            case "/updateCL":
                Client.clientWindow.refreshUserList(serverMessage);
                break;

                //someone whispered to you
            case "/w":
                Client.clientWindow.appendMessage(serverMessage, "whisper");
                try{
                    if(currentRunningGame == 1){
                        Client.game1.appendMessage(serverMessage, "whisper");
                    }else if(currentRunningGame == 2){
                        Client.game2.appendMessage(serverMessage, "whisper");
                    }
                }catch(Exception e){

                }
                break;

                //incoming draw in a game
            case "/draw":
                try{
                    //TODO: need to somehow handle the different games here
                    //System.out.println("move incoming -> " + serverMessage);

                    if(currentRunningGame == 1){
                        Client.game1.draw(Integer.parseInt(serverMessage.substring(0,1)));
                    }else if(currentRunningGame == 2){
                        Client.game2.draw(serverMessage);
                    }
                }catch(Exception e){
                    e.printStackTrace();
                }
                break;

                //your opponent surrendered
            case "/surrender":
                try{
                    //TODO: need to somehow handle the different games here
                    //System.out.println("move incoming -> " + serverMessage);

                    if(currentRunningGame == 1){
                        Client.game1.terminateGame(true);
                        Client.game1.appendMessage("Your opponent surrendered. ", "system");
                    }else if(currentRunningGame == 2){
                        Client.game2.terminateGame(true);
                        Client.game2.appendMessage("Your opponent surrendered. ", "system");
                    }
                    //Client.game2.
                }catch(Exception e){
                    e.printStackTrace();
                }
                break;

                //starts the game
            case "/start":
                if(serverMessage.charAt(0) == '1'){
                    //start game 1
                    System.out.println("Starting game 1.");
                    //maybe put that in the ClientWindow as well
                    currentRunningGame = 1;

                    //System.out.println("Msg = " + serverMessage);

                    try{
                        serverMessage = serverMessage.substring(2);
                    }catch(Exception e){

                    }

                    String[] gameInfo = serverMessage.split(" ");

                    String opponentName = gameInfo[0];
                    String playerName = gameInfo[1];
                    Integer chipNumber = Integer.parseInt(gameInfo[2]);

                    Thread game1Thread = new Thread(){
                        public void run(){
                            Client.game1 = new ClientGame1(socket, output, writer, opponentName,playerName, chipNumber);
                            Client.game1.createFrame(Client.game1);
                        }
                    };

                    game1Thread.run();
                }else if(serverMessage.charAt(0) == '2'){
                    System.out.println("Starting game 2.");
                    currentRunningGame = 2;

                    try{
                        serverMessage = serverMessage.substring(2);
                    }catch(Exception e){

                    }

                    String[] gameInfo = serverMessage.split(" ");

                    String opponentName = gameInfo[0];
                    String playerName = gameInfo[1];
                    Integer playerNumber = Integer.parseInt(gameInfo[2]);

                    Thread game2Thread = new Thread(){
                        public void run(){
                            Client.game2 = new ClientGame2(socket, output, writer, opponentName, playerName, playerNumber);
                            Client.game2.createFrame(Client.game2);
                        }
                    };

                    game2Thread.run();

                }
                break;

                //no command
            default:
                Client.clientWindow.appendMessage(serverMessage,"");
        }

    }

}
