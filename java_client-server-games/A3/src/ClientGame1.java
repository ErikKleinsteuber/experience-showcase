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

public class ClientGame1 extends JPanel {

    String assetspath = "C:\\Users\\Flat Erik\\Desktop\\Erfahrungssammlung\\[PROGPRAG]Programmierpraktikum\\A3\\Assets\\";
    JFrame myFrame;
    BufferedImage redcoin,bluecoin,gamefield,arrow,bg;
    boolean drawing = true;
    boolean running = true;
    Integer[][] board;
    Socket socket;
    OutputStream output;
    PrintWriter writer;
    String opponentName,playerName;
    Integer chipNumber;
    int falling = -1;
    int highestChip = -1;
    float speed = 0.0f;
    float dropdownPos = 0;

    JLabel opponentLabel;
    JLabel playerLabel;
    JLabel turnLabel;

    //zum Schreiben von Nachrichten
    JTextPane inputPane = new JTextPane();
    JScrollPane inputSP = new JScrollPane(inputPane);

    //zeigt den Chatverlauf
    JTextPane chatPane = new JTextPane();;
    JScrollPane chatSP = new JScrollPane(chatPane);

    JLabel[] arrowLabels;
    JButton surrenderButton = new JButton("Surrender");

    @Override
    public void paintComponent(Graphics g){
        super.paintComponent(g);
        g.drawImage(bg,0,0,this.getWidth(),this.getHeight(),null);
        //TODO: check why game gets repainted so often and see if can find solution
            //arrows
            int counter = 0;

            for(JLabel arrow : arrowLabels){
                if(running) {
                    if (drawing) {
                        arrow.setVisible(true);
                        if (checkIfMovePossible(counter)) {
                            arrow.setBounds(62 + (counter * 64), 0, arrow.getWidth(), arrow.getHeight());
                        } else {
                            arrow.setVisible(false);
                        }
                    } else {
                        arrow.setVisible(false);
                    }
                    counter++;
                }else{
                    arrow.setVisible(false);
                }
            }

        for(int y = 0; y < 4;y++){
            for(int x = 0; x< 9; x++){
                if(board[x][y] == 1){
                    if(falling>=0 && highestChip == y && falling == x){
                        dropdownPos += speed;
                        g.drawImage(redcoin,62+ (x*64),(int)(dropdownPos),redcoin.getWidth(),redcoin.getHeight(),null);
                        //System.out.println(speed);
                        if(dropdownPos >= 102+ (y*64)){
                            dropdownPos = 102+ (y*64);
                            speed = -0.9f*speed;
                            //System.out.println("groundhit + speed = " + speed);
                            if(Math.abs(speed) <0.5){
                                falling = -1;
                                highestChip = -1;
                                speed = 0.0f;
                                dropdownPos = 0;
                            }
                        }
                        speed += 0.01;
                    }else{
                        g.drawImage(redcoin,62+ (x*64),102+ (y*64),redcoin.getWidth(),redcoin.getHeight(),null);
                    }
                }else if(board[x][y] == 2){
                    if(falling>=0 && highestChip == y && falling == x){
                        dropdownPos += speed;
                        g.drawImage(bluecoin,62+ (x*64),(int)(dropdownPos),bluecoin.getWidth(),bluecoin.getHeight(),null);
                        //System.out.println(speed);
                        if(dropdownPos >= 102+ (y*64)){
                            dropdownPos = 102+ (y*64);
                            speed = -0.9f*speed;
                            //System.out.println("groundhit + speed = " + speed);
                            if(Math.abs(speed) <0.5){
                                falling = -1;
                                highestChip = -1;
                                speed = 0.0f;
                                dropdownPos = 0;
                            }
                        }
                        speed += 0.01;
                    }else{
                        g.drawImage(bluecoin,62+ (x*64),102+ (y*64),bluecoin.getWidth(),bluecoin.getHeight(),null);
                    }
                }
            }
        }

        //board
        g.drawImage(gamefield,0,0,gamefield.getWidth(),gamefield.getHeight(),null);

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

        if(falling>=0){
            this.repaint();
        }
    }

    public int getHighestChip(int column){
        for (int y = 0;y<4; y++){
            if(board[column][y] != 0){
                return y;
            }
        }
        return 3;
    }

    public void createFrame(ClientGame1 game1){
        initGame();
        if (chipNumber == 2){
            drawing = false;
        }
        try{
            redcoin = ImageIO.read(new File(assetspath + "redcoin64.png"));
            bluecoin = ImageIO.read(new File(assetspath + "bluecoin64.png"));
            gamefield = ImageIO.read(new File(assetspath + "gamefield.png"));
            arrow = ImageIO.read(new File(assetspath + "arrow.png"));
            bg = ImageIO.read(new File(assetspath + "landscape.png"));
            System.out.println("Assets loaded succesfully.");
        }catch(IOException io){
            System.out.println("Loading Assets failed.");
        }

        ImageIcon arrowIcon = new ImageIcon(arrow);
        arrowLabels = new JLabel[9];

        for(int x = 0; x<9; x++){
            JLabel arrowLabel = new JLabel();
            arrowLabel.setIcon(arrowIcon);
            arrowLabel.setCursor(new Cursor(Cursor.HAND_CURSOR));

            Integer move = x;

            arrowLabel.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    draw(move);
                }

            });

            arrowLabels[x] = arrowLabel;
            this.add(arrowLabel);
        }

        //region creating Frame
        myFrame = new JFrame();
        myFrame.add(game1);
        //size does not match the background picture for what reason ever... but i think its no problem
        myFrame.setPreferredSize(new Dimension(720,600));
        myFrame.setVisible(true);
        this.setPreferredSize(new Dimension(720,600));
        this.setLayout(null);
        myFrame.pack();

        myFrame.setResizable(false);

        turnLabel = new JLabel("Player's turn:");
        playerLabel = new JLabel(playerName);
        opponentLabel = new JLabel(opponentName);

        playerLabel.setOpaque(true);
        opponentLabel.setOpaque(true);

        if(chipNumber == 1){
            playerLabel.setBackground(new Color(255,0,0));
            opponentLabel.setBackground(new Color(0,0,255));
        }else if(chipNumber == 2){

            playerLabel.setBackground(new Color(0,0,255));
            opponentLabel.setBackground(new Color(255,0,0));
        }

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
    }

    public void surrender(){
        writer.println("/surrender");
        terminateGame(false);
    }

    public void initGame(){
        board = new Integer[9][4];
        for(int y = 0; y < 4;y++){
            for(int x = 0; x< 9; x++){
                board[x][y] = 0;
            }
        }
    }

    public void printBoard(){
        for(int y = 0; y < 4;y++){
            for(int x = 0; x< 9; x++){
                System.out.print(board[x][y]);
            }
            System.out.println();
        }
    }

    public void draw(Integer move){

        if(running){
            //System.out.println("drawing = " + drawing + " MovePoss = " + checkIfMovePossible(move) + " move = " + move);
            if(drawing){
                if (checkIfMovePossible(move)){
                    writer.println("/draw " + move);
                    simulateDraw(move);
                    drawing = false;
                }else{
                    //move not possible
                }
            }else{
                //not your turn
                if (checkIfMovePossible(move)){
                    simulateDraw(move);
                    drawing = true;
                }else{
                    //move not possible
                }
            }
        }
    }

    public void simulateDraw(Integer move){
        for (int y = 3; y >= 0; y--){
            if (board[move][y] == 0){
                if(drawing){
                    board[move][y] = chipNumber;
                    //System.out.println("win = " + validateWin(chipNumber));
                    if(validateWin(chipNumber)){
                        terminateGame(true);
                    }
                }else{
                    if(chipNumber == 2){
                        board[move][y] = 1;
                        //System.out.println("win = " + validateWin(1));
                        if(validateWin(1)){
                            terminateGame(false);
                        }
                    }else{
                        board[move][y] = 2;
                        //System.out.println("win = " + validateWin(2));
                        if(validateWin(2)){
                            terminateGame(false);
                        }
                    }
                }
                falling = move;
                if(falling>=0){
                    highestChip = getHighestChip(falling);
                    speed = 0.0f;
                    dropdownPos = 0;
                }
                break;
            }
        }
        //printBoard();
        this.repaint();
    }

    public boolean checkIfMovePossible(Integer move){
        if(move >= 0 && move <= 8 && board[move][0] == 0){
            return true;
        }else{
            return false;
        }
    }

    boolean validateWin(int move){
        int wincondition = 0;
        for(int x = 0; x <9; x++){
            for(int y = 0; y < 4; y++){
                try{
                    for(int z = 0;z < 4; z++){
                        if(board[x+z][y+z]==move){
                            wincondition += 1;
                            if(wincondition == 4){
                                return true;
                            }
                        }else{
                            break;
                        }
                    }
                }catch(ArrayIndexOutOfBoundsException e){

                }
                wincondition = 0;
                try{
                    for(int z = 0;z < 4; z++){
                        if(board[x][y+z]==move){
                            wincondition += 1;
                            if(wincondition == 4){
                                return true;
                            }
                        }else{
                            break;
                        }
                    }
                }catch(ArrayIndexOutOfBoundsException e){

                }
                wincondition = 0;
                try{
                    for(int z = 0;z < 4; z++){
                        if(board[x+z][y]==move){
                            wincondition += 1;
                            if(wincondition == 4){
                                return true;
                            }
                        }else{
                            break;
                        }
                    }
                }catch(ArrayIndexOutOfBoundsException e){

                }
                wincondition = 0;
                try{
                    for(int z = 0;z < 4; z++){
                        if(board[x+z][y-z]==move){
                            wincondition += 1;
                            if(wincondition == 4){
                                return true;
                            }
                        }else{
                            break;
                        }
                    }
                }catch(ArrayIndexOutOfBoundsException e){

                }
                wincondition = 0;

            }
        }
        return false;
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
            writer.println("/end");
        }
    }

    public static void main(String[] args) {
        ClientGame1 game = new ClientGame1(new Socket(),null,null,null,null,1);
        game.createFrame(game);
    }

    public ClientGame1(Socket socket, OutputStream output, PrintWriter writer, String opponentName, String playerName, Integer chipNumber){
        this.socket = socket;
        this.output = output;
        this.writer = writer;
        this.opponentName = opponentName;
        this.playerName = playerName;
        this.chipNumber = chipNumber;
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

}

