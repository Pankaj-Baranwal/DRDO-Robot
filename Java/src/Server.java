import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by karan on 28/1/17.
 */
public class Server {

    public static void main(String[] args) throws IOException {
        ServerSocket Data_Server_socket=new ServerSocket(6555);//Data Port
        ServerSocket File_Server_socket=new ServerSocket(6556);//File Port
        Thread_management thread_management=new Thread_management();
        int i=0;
        while (true){
            Thread_management.Data_Socket =Data_Server_socket.accept();
            FileServer.file_Socket=File_Server_socket.accept();
            thread_management.start();
            System.out.println("Connected to "+(i+1)+"th Client");
        i++;
        }



    }
}
