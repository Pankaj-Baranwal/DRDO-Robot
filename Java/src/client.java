import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

/**
 * Created by karan on 29/1/17.
 */
public class client {
    public static void main(String[] args) throws IOException {

        Socket s=new Socket("10.42.0.221",6555);
        DataInputStream stream=new DataInputStream(s.getInputStream());
        DataOutputStream outputStream=new DataOutputStream(s.getOutputStream());
        Scanner scanner=new Scanner(System.in);
        while (true) {
            for (int i = 0; i < 4; i++) {
                outputStream.writeInt(scanner.nextInt());
            }
        outputStream.flush();
        }
    }
}
