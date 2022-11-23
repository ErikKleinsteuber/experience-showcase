import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;

public class ClientWindow extends JPanel {

    //TODO:     Styling
    //TODO:     On_CLOSE
    //TODO:     BUGS:
    //              - when you doubleclick autoresize the frame, the textpanes are not immediatly
    //              resized with their scrollpanes, they need at least one change or input to resize after that
    //TODO: if "\n" is part of the message, it gets split into more messages (dont't know why yet)
    //      siehe TODO #1 in ServerThread (dort sollte das Problem liegen)
    //TODO: start game and connect to other player
    //TODO: chat does not scroll down

    BufferedImage image;
    JFrame myFrame;

    //zum Schreiben von Nachrichten
    JTextPane inputPane = new JTextPane();
    JScrollPane inputSP = new JScrollPane(inputPane);

    //zeigt den Chatverlauf
    JTextPane chatPane = new JTextPane();;
    JScrollPane chatSP = new JScrollPane(chatPane);

    //clientList (Zeigt die Namen aller angemeldeter Benutzer)
    JTextPane clientlistPane = new JTextPane();
    JScrollPane clientlistSP = new JScrollPane(clientlistPane);

    //zeigt die Spieleinladungen an
    JTextPane invitationsPane = new JTextPane();
    JScrollPane invitationsSP = new JScrollPane(invitationsPane);

    JLabel chatLabel = new JLabel("Chat:");
    JLabel clientsLabel = new JLabel("Online:");

    OutputStream output;
    PrintWriter writer;

    @Override
    public void paintComponent(Graphics g){
        super.paintComponent(g);

        //Hintergrund
        g.drawImage(image, 0,0,this.getSize().width,this.getSize().height,null);

        //region dynamische Skalierung der Komponenten
        //chatPane.setBounds(12,12,(int)(this.getSize().width/1.4),(int)(this.getSize().height/1.2));
        chatLabel.setBounds(12,12,50,20);
        chatSP.setBounds(12,32,(int)(this.getSize().width/1.4),(int)(this.getSize().height/1.2)-20);
        inputSP.setBounds(12,(int)(this.getSize().height/1.2)+13,(int)(this.getSize().width/1.4),
                this.getSize().height-((int)(this.getSize().height/1.2)+13));
        clientsLabel.setBounds((int)(this.getSize().width/1.4) + 13,12,750,20);
        clientlistSP.setBounds((int)(this.getSize().width/1.4) + 13, 32,
                this.getSize().width - ((int)(this.getSize().width/1.4) + 13 + 1), (int)((this.getSize().height-33)));
        //invitationsSP.setBounds((int)(this.getSize().width/1.4) + 13, (int)((this.getSize().height-24)/2.0)+32,
        //        this.getSize().width - ((int)(this.getSize().width/1.4) + 13 + 1),(int)((this.getSize().height)/2.0)-20);
        //endregion
    }

    public void createFrame(ClientWindow clientWindow){
        //TODO: maybe javax.swing.SwingUtilities.invokeLater(new Runnable() { -> siehe stackoverflow thread

        //region creating Frame
        myFrame = new JFrame();
        myFrame.add(clientWindow);
        myFrame.setPreferredSize(new Dimension(640,480));
        myFrame.setVisible(true);
        myFrame.pack();

        myFrame.addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                writer.println("/logout");
                System.exit(0);
            }
        });
        //endregion

        //lade Hintergrundbild
        try{
            image = ImageIO.read(new File("C:\\Users\\Flat Erik\\Desktop\\Erfahrungssammlung\\[PROGPRAG]Programmierpraktikum\\A3\\Assets\\landscape.png"));
        }catch(IOException io){
            System.out.println("Hintergrundbild in ClientWindow -> createFrame() konnte nicht geladen werden.");
            System.out.println(io);
        }

        //region Style, Transparenz und Editierbarkeit
        this.setLayout(null);
        this.setOpaque(false);

        inputPane.setOpaque(false);
        inputSP.setOpaque(false);
        inputSP.getViewport().setOpaque(false);

        inputPane.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        inputPane.setForeground(Color.BLACK);

        chatLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        chatPane.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        chatPane.setForeground(Color.BLACK);

        clientsLabel.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        clientlistPane.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        clientlistPane.setForeground(Color.BLACK);

        invitationsPane.setFont(new Font("Comic Sans MS", Font.PLAIN, 16));
        invitationsPane.setForeground(Color.BLACK);

        invitationsPane.setOpaque(false);
        invitationsSP.setOpaque(false);
        invitationsSP.getViewport().setOpaque(false);

        chatPane.setOpaque(false);
        chatSP.setOpaque(false);
        chatSP.getViewport().setOpaque(false);

        //automatically scrolls the pane further down if a new message comes in (maybe later also try to prevent that
        //if client scrolled up)
        DefaultCaret caret = (DefaultCaret)chatPane.getCaret();
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);

        //TODO -> scrollt nicht
        chatSP.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);

        clientlistPane.setOpaque(false);
        clientlistSP.setOpaque(false);
        clientlistSP.getViewport().setOpaque(false);

        this.add(inputSP);
        this.add(chatSP);
        this.add(clientlistSP);
        this.add(invitationsSP);
        this.add(chatLabel);
        this.add(clientsLabel);

        //die beiden sollen nicht editierbar sein
        chatPane.setEditable(false);
        clientlistPane.setEditable(false);
        invitationsPane.setEditable(false);

        myFrame.pack();
        //endregion

        //notwendig damit das fenster einmal zu Beginn gezeichnet wird
        this.repaint();

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
                writer.println(inputPane.getText());
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
        //endregion

    }

    public void setOutStream(OutputStream output, PrintWriter writer){
        //kopiere die Streams aus Client() um sie hier zu benutzen
        this.output = output;
        this.writer = writer;
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

    public void refreshUserList(String allUsers){
        //allUsers ... String aller Nutzernamen der Nutzer die gerade online sind, getrennt durch " "

        //split(" ") und erzeuge ein Array mit Element = Nutzername
        String[] allUsersList = allUsers.split(" ");

        try{
            //entfernt das alte Panel, falls es eins gibt
            clientlistPane.getDocument().remove(0,1);
        }catch(BadLocationException badLoc){
            //handle Error
        }

        //Panel zur korrekten Darstellung der labels
        JPanel panel = new JPanel();

        //transparent und übereinander gestapelt
        panel.setOpaque(false);
        panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));

        //ein Label mit Popupmenu pro Nutzer
        for (String name : allUsersList){
            JLabel label = new JLabel(name);
            label.setFont(clientlistPane.getFont());
            label.setText(name);
            label.setCursor(new Cursor(Cursor.HAND_CURSOR));

            JMenuItem invite1 = new JMenuItem("Invite to 4-Gewinnt");
            JMenuItem invite2 = new JMenuItem("Invite to Futtern");
            JMenuItem accept = new JMenuItem("Accept Invite");
            JMenuItem whisper = new JMenuItem("Whisper");

            JPopupMenu menu = new JPopupMenu();
            menu.add(invite1);
            menu.add(invite2);
            menu.add(whisper);
            menu.add(accept);

            label.setComponentPopupMenu(menu);

            invite1.addActionListener(event -> {
                //supercast um von dem Menuitem den Text des Labels zu bekommen
                inviteToGame1(((JLabel)((JPopupMenu)((JMenuItem) event.getSource()).getParent()).getInvoker()).getText());
            });

            invite2.addActionListener(event -> {
                inviteToGame2(((JLabel)((JPopupMenu)((JMenuItem) event.getSource()).getParent()).getInvoker()).getText());
            });

            accept.addActionListener(event -> {
                acceptInvite(((JLabel)((JPopupMenu)((JMenuItem) event.getSource()).getParent()).getInvoker()).getText());
            });

            whisper.addActionListener(event -> {
                infuseWhisper(((JLabel)((JPopupMenu)((JMenuItem) event.getSource()).getParent()).getInvoker()).getText());
            });

            panel.add(label);
        }

        //clientlistPane.add(panel,BorderLayout.LINE_START);     //nicht nötig soweit ich weiß
        clientlistPane.insertComponent(panel);
    }

    public void acceptInvite(String user){
        writer.println("/yes " + user);
    }

    public void inviteToGame1(String user){
        writer.println("/invite " + user + " 1");
    }

    public void inviteToGame2(String user){
        writer.println("/invite " + user + " 2");
    }

    public void infuseWhisper(String name){
        inputPane.setText("/w " + name + " ");
    }

    //gets called when you doubleclick resize or maximize the frame
    @Override
    public void setSize(int width, int height) {
        super.setSize(width, height);
        this.repaint();
    }

    @Override
    public void setBounds(Rectangle r) {
        super.setBounds(r);
    }

    @Override
    public void setBounds(int x, int y, int width, int height) {
        super.setBounds(x, y, width, height);
    }
}