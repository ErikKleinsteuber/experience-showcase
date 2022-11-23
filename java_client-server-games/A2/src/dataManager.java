import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

public class dataManager {

    //Properties: https://stackoverflow.com/questions/13597476/save-hashmap-properties-to-a-properties-file-and-load-those-properties-back-to

    private synchronized Map<String,String> getLoginData() throws IOException{
        Map<String, String> loginData = new HashMap<String, String>();
        Properties properties = new Properties();

        properties.load(new FileInputStream("C:\\My_stuff\\Studium\\[PROGPRAG]Programmierpraktikum\\A2\\Assets\\ldata.properties"));

        for (String key : properties.stringPropertyNames()) {
            loginData.put(key, properties.get(key).toString());
        }

        return loginData;
    }

    //TODO: if username does not match, make a new entry with the password he did send
    //checks if user is already registered (username found) and if the password (which the client typed in) matches the username
    public synchronized boolean checkAcces(String username, String password){

        //System.out.println("username=" + username + "||password=" + password);

        try{
            if (getLoginData().get(username).equals(password)){
                return true;
            }else{
                return false;
            }
        }catch(IOException ex){
            ex.printStackTrace();
        }

        //failed loading the loginData if reached this statement
        return false;
    }

    public synchronized boolean checkIfUserExists(String userName){
        try{
            if(getLoginData().get(userName) == null){
                return false;
            }else{
                return true;
            }
        }catch(IOException ex){
            ex.printStackTrace();
        }

        //if this statement is reached, data could not be loaded
        return true;
    }

    public synchronized boolean createAccount(String userName, String password) {
        try{
            Map<String, String> loginData = getLoginData();
            if(!checkIfUserExists(userName)){
                loginData.put(userName,password);
            }else{
                System.out.println("User already exists!");
                return false;
            }

            Properties properties = new Properties();

            //test Data -> hardcoded
            //loginData.put("peter", "123");
            //loginData.put("nils", "eyesky");
            //loginData.put("erik", "tegut");
            //loginData.put("moira", "pc");
            //loginData.put("fritz","earth");

            properties.putAll(loginData);
            properties.store(new FileOutputStream("C:\\My_stuff\\Studium\\[PROGPRAG]Programmierpraktikum\\A2\\Assets\\ldata.properties"), null);
            return true;

        }catch(IOException ex){
            ex.printStackTrace();
        }

        //something went wrong
        return false;
    }

}
