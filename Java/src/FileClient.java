import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.Socket;

/**
 * Created by karan on 30/1/17.
 */
public class FileClient {
    public static void main(String[] srgs) throws IOException {
        Socket s=new Socket("10.42.0.221",6556);
        InputStream inputStream=s.getInputStream();

        while (true) {
            FileOutputStream writer=new FileOutputStream(new File("temp.jpg"));
            int t;
            System.out.println("ffdddfdf");
            byte[] arr=new byte[8192];
            while ((t=inputStream.read(arr))!=-1){
                System.out.println(t);
                if(t==1&&(arr[0]==-1))
                    break;
                writer.write(arr,0,t);
            }
            writer.flush();
            writer.close();
            System.out.println("wriiter");
            BufferedImage image=ImageIO.read(new File("temp.jpg"));
            JFrame frame = new JFrame();
            JLabel label = new JLabel(new ImageIcon(image));
            frame.getContentPane().add(label, BorderLayout.CENTER);
            frame.pack();
            frame.setVisible(true);
        }

    }
}
