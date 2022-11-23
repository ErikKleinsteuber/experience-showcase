import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class ClientGame2 extends JPanel {

    String assetspath = "C:\\Users\\Flat Erik\\Desktop\\Erfahrungssammlung\\[PROGPRAG]Programmierpraktikum\\A3\\Assets\\";

    Socket socket;
    OutputStream output;
    PrintWriter writer;
    String opponentName,playerName;
    Integer playerNumber;
    JFrame myFrame;

    boolean drawing = true;
    boolean running = true;

    Integer[][] board;

    BufferedImage tile,warntile,markedtile,bluetile,redtile,bg;

    String hover = "";

    JLabel opponentLabel;
    JLabel playerLabel;
    JLabel turnLabel;

    //zum Schreiben von Nachrichten
    JTextPane inputPane = new JTextPane();
    JScrollPane inputSP = new JScrollPane(inputPane);

    //zeigt den Chatverlauf
    JTextPane chatPane = new JTextPane();;
    JScrollPane chatSP = new JScrollPane(chatPane);

    JLabel[][] tileLabels;
    JButton surrenderButton = new JButton("Surrender");

    @Override
    public void paintComponent(Graphics g){
        super.paintComponent(g);
        g.drawImage(bg,0,0,this.getWidth(),this.getHeight(),null);

        for(int y = 0; y < 8; y++){
            for(int x = 0; x < 14; x++){
                        if(board[x][y] == 0){
                            tileLabels[x][y].setVisible(true);
                            tileLabels[x][y].setBounds(119 + (x*33),50+(y*33), tileLabels[x][y].getWidth(),tileLabels[x][y].getHeight());

                            //TODO: maybe later hover effect
                            /*
                            if(!(hover.equals(""))){
                                if(Integer.parseInt(getMove(hover)[0])<=x && Integer.parseInt(getMove(hover)[1])<=y){
                                    System.out.println(hover);
                                    tileLabels[x][y].setVisible(false);
                                    g.drawImage(markedtile,1 + (x*33),1+(y*33), markedtile.getWidth(),
                                            markedtile.getHeight(),null);
                                    tileLabels[x][y].setVisible(true);
                                }
                            }*/
                        }else if(board[x][y] == 3){
                            tileLabels[x][y].setVisible(false);
                            //System.out.println(x + " " + y);
                            g.drawImage(warntile,119 + (x*33),50+(y*33), warntile.getWidth(),warntile.getHeight(),null);
                        }else if(board[x][y] == 1){
                            tileLabels[x][y].setVisible(false);
                            g.drawImage(redtile,119 + (x*33),50+(y*33), redtile.getWidth(),redtile.getHeight(),null);
                        }else if(board[x][y] == 2){
                            tileLabels[x][y].setVisible(false);
                            g.drawImage(bluetile,119 + (x*33),50+(y*33), bluetile.getWidth(),bluetile.getHeight(),null);
                        }
                        //System.out.print(board[x][y]);
            }
            //System.out.println();
        }

        turnLabel.setBounds(10,10,75,20);
        opponentLabel.setBounds(10,30,50,20);
        playerLabel.setBounds(10,51,50,20);

        if(running){
            if(drawing){
                playerLabel.setVisible(true);
                opponentLabel.setVisible(false);
            }else{
                playerLabel.setVisible(false);
                opponentLabel.setVisible(true);
            }
        }else{
            playerLabel.setVisible(false);
            opponentLabel.setVisible(false);
            turnLabel.setText("Game Over.");
        }

        //chat
        chatSP.setBounds(50,381,600,120);
        inputSP.setBounds(50,502,500,40);

        if(running){
            surrenderButton.setBounds(551,502,100,40);
        }else{
            surrenderButton.setVisible(false);
        }

        //TODO: maybe later hover effect
        //if(!(hover.equals(""))){
        //    this.repaint();
        //}
    }

    public void createFrame(ClientGame2 game){

        initGame();
        if(playerNumber == 2){
            drawing = false;
        }

        try{
            tile = ImageIO.read(new File(assetspath + "tile.png"));
            warntile = ImageIO.read(new File(assetspath + "warntile.png"));
            markedtile = ImageIO.read(new File(assetspath + "markedtile.png"));
            redtile = ImageIO.read(new File(assetspath + "redtile.png"));
            bluetile = ImageIO.read(new File(assetspath + "bluetile.png"));
            bg = ImageIO.read(new File(assetspath + "landscape.png"));

            System.out.println("Loaded Assets succesfully");
        }catch(IOException ioex){
            System.out.println("Failed at loading Assets.");
        }

        turnLabel = new JLabel("Player's turn:");
        playerLabel = new JLabel(playerName);
        opponentLabel = new JLabel(opponentName);

        playerLabel.setOpaque(true);
        opponentLabel.setOpaque(true);

        if(playerNumber == 1){
            playerLabel.setBackground(new Color(255,0,0));
            opponentLabel.setBackground(new Color(0,0,255));
        }else if(playerNumber == 2){

            playerLabel.setBackground(new Color(0,0,255));
            opponentLabel.setBackground(new Color(255,0,0));
        }

        ImageIcon arrowIcon = new ImageIcon(tile);
        tileLabels = new JLabel[14][8];

        for(int x = 0; x < 14; x++){
            for(int y = 0; y < 8; y++){
                JLabel tileLabel = new JLabel();
                tileLabel.setIcon(arrowIcon);
                tileLabel.setCursor(new Cursor(Cursor.HAND_CURSOR));

                String move = x + " " + y;

                tileLabel.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent e) {
                        if(running){
                            if(drawing){
                                System.out.println("Move: " + move);
                                draw(move);
                            }
                        }
                    }

                    @Override
                    public void mouseEntered(MouseEvent e) {
                        super.mouseEntered(e);
                        //hover = move;
                        ((JPanel)(((JLabel)(e.getSource())).getParent())).repaint();
                    }

                    @Override
                    public void mouseExited(MouseEvent e) {
                        super.mouseExited(e);
                        //hover = "";
                    }

                });

                tileLabels[x][y] = tileLabel;
                this.add(tileLabel);
            }
        }

        //region creating Frame
        myFrame = new JFrame();
        myFrame.add(game);
        //size does not match the background picture for what reason ever... but i think its no problem
        myFrame.setPreferredSize(new Dimension(720,600));
        myFrame.setVisible(true);
        this.setPreferredSize(new Dimension(720,600));
        this.setLayout(null);
        myFrame.pack();

        myFrame.setResizable(false);

        chatPane.setOpaque(false);
        chatSP.setOpaque(false);
        chatSP.getViewport().setOpaque(false);

        inputPane.setOpaque(false);
        inputSP.setOpaque(false);
        inputSP.getViewport().setOpaque(false);

        surrenderButton.addActionListener((new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                surrender();
            }
        }));

        this.add(surrenderButton);
        this.add(chatSP);
        this.add(inputSP);
        this.add(playerLabel);
        this.add(opponentLabel);
        this.add(turnLabel);

        //region logic for keybindings in the inputPane
        int condition = JComponent.WHEN_FOCUSED;
        InputMap iMap = inputPane.getInputMap(condition);
        InputMap iMap2 = inputPane.getInputMap(condition);
        ActionMap aMap = inputPane.getActionMap();

        String enter = "enter";
        String shiftenter = "shiftenter";
        iMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), enter);
        iMap2.put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, KeyEvent.SHIFT_DOWN_MASK), shiftenter);

        //Event for Enter
        aMap.put(enter, new AbstractAction() {

            @Override
            public void actionPerformed(ActionEvent arg0) {
                writer.println("/w " + opponentName + " " + inputPane.getText());
                inputPane.setText("");
            }
        });

        //Event for shift+Enter
        aMap.put(shiftenter, new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                inputPane.setText(inputPane.getText() + "\n");
            }
        });

        this.repaint();
    }

    public void initGame(){

        board = new Integer[14][8];
        for(int x = 0; x < 14; x++){
            for(int y = 0; y < 8; y++){
                    board[x][y] = 0;
            }
        }

        board[0][0] = 3;

    }

    public void surrender(){
        writer.println("/surrender");
        terminateGame(false);
    }

    public boolean validateGame(){
        for(int x = 0; x < 14; x++){
            for(int y = 0; y < 8; y++){
                if(board[x][y] == 0){
                    return false;
                }
            }
        }
        return true;
    }

    public void draw(String move){

        String[] moves = getMove(move);

        if(running){
            //System.out.println("drawing = " + drawing + " MovePoss = " + checkIfMovePossible(move) + " move = " + move);
            if(drawing){
                if (checkIfMovePossible(move)){
                    writer.println("/draw " + move);
                    simulateDraw(move);
                    if(validateGame()){
                        terminateGame(true);
                    }
                    drawing = false;
                }else{
                    //move not possible
                }
            }else{
                //not your turn
                if (checkIfMovePossible(move)){
                    simulateDraw(move);
                    if(validateGame()){
                        terminateGame(false);
                    }
                    drawing = true;
                }else{
                    //move not possible
                }
            }
        }
    }

    public String[] getMove(String move){
        String[] moves = move.split(" ");
        return moves;
    }

    public boolean checkIfMovePossible(String move){
        return true;
    }

    public void simulateDraw(String move){
        String[] moves = getMove(move);
        System.out.println("Move in draw: " + moves[0] + " " + moves[1]);

        for(int y = 0; y < 8; y++){
            for(int x = 0; x < 14; x++){
                if(board[x][y] == 0 && x >= Integer.parseInt(moves[0]) && y >= Integer.parseInt(moves[1])){
                    if(drawing){
                        board[x][y] = playerNumber;
                    }else{
                        if(playerNumber == 1){
                            board[x][y] = 2;
                        }else{
                            board[x][y] = 1;
                        }
                    }
                }
            }
        }

        printBoard();

        this.repaint();
    }

    public void printBoard(){
        for(int y = 0; y < 8; y++){
            for(int x = 0; x < 14; x++){
                System.out.print(board[x][y]);
            }
            System.out.println();
        }
    }

    public void terminateGame(boolean won){
        if(running){
            drawing = false;
            running = false;
            if(won){
                appendMessage("You won ", "system");
            }else{
                appendMessage("You lost. ", "system");
            }
            this.repaint();
            ClientThread.currentRunningGame = 0;
            writer.println("/surrender");
            writer.println("/end");
        }
    }

    public void appendMessage(String message, String type){
        //type can be "user"(black) or "system"(green) or "error"(red)
        message = message + "\n";

        //defines the style for the Component which is added to the textPane
        SimpleAttributeSet style = new SimpleAttributeSet();

        if(type.equals("system")){
            StyleConstants.setForeground(style,Color.GREEN);
        }else if(type.equals("error")){
            StyleConstants.setForeground(style,Color.RED);
        }else if(type.equals("whisper")){
            StyleConstants.setForeground(style,Color.MAGENTA);
        }

        try {
            //adding the message to the chatPane (displaying it to the Client)
            chatPane.getStyledDocument().insertString(chatPane.getStyledDocument().getLength(), message, style);
        }catch(BadLocationException e){
            //error handling
        }
    }

    public ClientGame2(Socket socket, OutputStream output, PrintWriter writer, String opponentName, String playerName, Integer playerNumber){

        this.socket = socket;
        this.output = output;
        this.writer = writer;
        this.opponentName = opponentName;
        this.playerName = playerName;
        this.playerNumber = playerNumber;
        System.out.println("OpponentName = " + opponentName);
        System.out.println("playerNumber = " + playerNumber);

    }

    public static void main(String[] args) {
        ClientGame2 game = new ClientGame2(new Socket(),null,null,null,null,1);
        game.createFrame(game);
    }

}
