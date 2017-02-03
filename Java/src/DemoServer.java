import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

/**
 * Created by karan on 30/1/17.
 */
public class DemoServer {
    public static void main(String[] args) throws IOException {
        ServerSocket socket=new ServerSocket(6556);
        Socket s=socket.accept();
        DataOutputStream dataOutputStream=new DataOutputStream(s.getOutputStream());
        Scanner scanner=new Scanner(System.in);
        while (true){
            dataOutputStream.writeUTF(scanner.nextLine());
        }
    }
}
