import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultCaret;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class ServerWindow extends JPanel {

    //TODO:     Styling

    BufferedImage bg;
    String assetspath = "C:\\My_stuff\\Studium\\[PROGPRAG]Programmierpraktikum\\A3\\Assets\\";

    //textPane für die Textdarstellung
    JTextPane consolePane = new JTextPane();

    //Scrollpane für die TextKonsole
    JScrollPane consoleSP = new JScrollPane(consolePane);

    JLabel consoleLabel = new JLabel("Console:");

    //Textpane für die clientList
    JTextPane clientlistPane = new JTextPane();

    //Scrollpane für die clientList
    JScrollPane clientlistSP = new JScrollPane(clientlistPane);

    JLabel clientLabel = new JLabel("Online:");

    //Textpane für die laufenden Spiele
    JTextPane gamesPane = new JTextPane();

    //Scrollpane für die laufenden Spiele
    JScrollPane gamesSP = new JScrollPane(gamesPane);

    JLabel gamesLabel = new JLabel("Games:");

    //Textpane für die laufenden Einladungen
    JTextPane invitationsPane = new JTextPane();

    //Scrollpane für die laufenden Einladungen
    JScrollPane invitationsSP = new JScrollPane(invitationsPane);

    JLabel invitLabel = new JLabel("Invitations:");

    JFrame frame = new JFrame();

    @Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);
        g.drawImage(bg,0,0,this.getWidth(),this.getHeight(),null);

        //TODO: maybe only calculate these when resizing and make variables

        //Dynamische Skalierung der Komponenten
        int consoleWidth = (int)(this.getSize().width/1.8);
        int consoleHeight = (int)(this.getSize().height/1.3);
        int clHeight = (int)(this.getSize().height/1.3);
        int clWidth = (int)((this.getSize().width - ((int)(this.getSize().width/1.8) + 13 + 1))/2.0);

        consoleLabel.setBounds(13,12,75,20);
        consoleSP.setBounds(12,32,consoleWidth,consoleHeight-20);

        clientLabel.setBounds(consoleWidth + 12 + 1,12,75,20);
        clientlistSP.setBounds(consoleWidth + 12 + 1, 32,
                clWidth, clHeight-20);

        gamesLabel.setBounds(clWidth + consoleWidth + 12 + 1 + 1,12,75,20);
        gamesSP.setBounds(clWidth + consoleWidth + 12 + 1 + 1,
                32,
                this.getSize().width - (clWidth + consoleWidth + 12 + 1 + 1 + 12),
                (int)((this.getSize().height/1.3)/2.0)-20);

        invitLabel.setBounds(clWidth + consoleWidth + 12 + 1 + 1,(int)((this.getSize().height/1.3)/2.0) + 1 + 22,100,20);
        invitationsSP.setBounds(clWidth + consoleWidth + 12 + 1 + 1,
                (int)((this.getSize().height/1.3)/2.0) + 1 + 42,
                this.getSize().width - (clWidth + consoleWidth + 12 + 1 + 1 + 12),
                (int)((this.getSize().height/1.3)/2.0)-30);

    }

    public void createServerWindow(ServerWindow serverWindow){

        try{
            bg = ImageIO.read(new File(assetspath + "desert.png"));
            System.out.println("Assets loaded succesfully.");
        }catch(IOException ioex){
            System.out.println("Failed loading assets.");
        }

        frame = new JFrame();
        frame.add(serverWindow);
        frame.setPreferredSize(new Dimension(1280,720));
        frame.setVisible(true);
        frame.pack();

        // windowClosing-Event anmelden
        frame.addWindowListener(new WindowAdapter()
        {
            public void windowClosing(WindowEvent e)
            {
                //TODO: rewrite that part and send a message to every client that the Server is shutting down

                try{
                    Server.serverSocket.close();
                }catch (IOException ioEx){
                    System.out.println("IOException while shutting down Server.");
                }
                System.exit(0);
            }
        });

        this.setLayout(null);

        consoleLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        clientLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        gamesLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        invitLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));


        clientlistPane.setEditable(false);
        consolePane.setEditable(false);
        gamesPane.setEditable(false);
        invitationsPane.setEditable(false);

        //TODO: stop from permascrolling
        DefaultCaret caret = (DefaultCaret)consolePane.getCaret();
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);
        consoleSP.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);

        //Scrollpane wird unserem Panel hinzugefügt
        this.add(consoleSP);
        this.add(clientlistSP);
        this.add(gamesSP);
        this.add(invitationsSP);
        this.add(consoleLabel);
        this.add(clientLabel);
        this.add(gamesLabel);
        this.add(invitLabel);

        frame.pack();

        this.repaint();

    }

    //schreibt messages in das textPane (eventuell noch farbe einstellen -> zweiter parameter)
    public void appendMessage(String message, String type){
        //type can be "user"(black) or "system"(green) or "error"(red)

        message = message + "\n";

        //defines the style for the Component wich is added to the textpane
        SimpleAttributeSet style = new SimpleAttributeSet();

        if(type.equals("system")){
            StyleConstants.setForeground(style,Color.GREEN);
        }

        if(type.equals("error")){
            StyleConstants.setForeground(style,Color.RED);
        }

        try {
            consolePane.getStyledDocument().insertString(consolePane.getStyledDocument().getLength(), message, style);
        }catch(BadLocationException e){
            //error handling
        }
    }

    public void refreshUserList(ArrayList<String> allUsers){
        String allUsersDisplay = "";

        for (String name : allUsers){
            allUsersDisplay = allUsersDisplay + name + "\n";
        }

        clientlistPane.setText(allUsersDisplay);
    }

    public void refreshInvitationsList(ArrayList<ArrayList<String>> invitationsList){
        String allInvitationsDisplay = "";

        for (ArrayList<String> data : invitationsList){
            allInvitationsDisplay = allInvitationsDisplay + data.get(0) + " -> " + data.get(1) + " " + data.get(2) + "\n";
        }

        invitationsPane.setText(allInvitationsDisplay);
    }

    public void refreshGamesList(ArrayList<ArrayList<String>> gamesList){
        String allGamesDisplay = "";

        for (ArrayList<String> data : gamesList){
            allGamesDisplay = allGamesDisplay + data.get(0) + " vs " + data.get(1) + " Game: " + data.get(2) + "\n";
        }

        gamesPane.setText(allGamesDisplay);
    }

}
