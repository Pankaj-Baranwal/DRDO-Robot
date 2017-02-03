import java.io.DataInputStream;
import java.io.File;
import java.io.IOException;
import java.net.Socket;

/**
 * Created by karan on 28/1/17.
 */
public class Thread_management extends Thread{

    static Socket Data_Socket;

    public void run(){

        try {
            System.out.println("In Thread");
            DataInputStream inputStream=new DataInputStream(Data_Socket.getInputStream());
            Raspberry_gpio gpio=new Raspberry_gpio();
            FileServer server=new FileServer();
            int control[]=new int[4];
            while (true) {
                control[0] = inputStream.readInt();
                control[1] = inputStream.readInt();
                control[2] = inputStream.readInt();
                control[3] = inputStream.readInt();
                System.out.println("Received Control Word "+control[0]+" "+control[1]+" "+control[2]+" "+control[3]);
                gpio.send_control_word(control);
                if(control[0]==1) {
                    gpio.wait_till_command_executed_on_firebird();
                    server.send_data();
                }
            }

        } catch (IOException | FailedToRunRaspistillException e) {
            e.printStackTrace();
        }


    }
}
