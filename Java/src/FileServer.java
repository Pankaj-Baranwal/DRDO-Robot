import java.io.*;
import java.net.Socket;

/**
 * Created by karan on 28/1/17.
 */
public class FileServer{

    static Socket file_Socket;
    RPiCamera piCamera=new RPiCamera("/home/karan/Pictures");
    private InputStream image_stream;
    OutputStream stream;

    public FileServer() throws FailedToRunRaspistillException {

    }

    public void send_data(){
        try {
            stream=file_Socket.getOutputStream();
            System.out.println("Sending image back, check it out");
            image_stream=piCamera.takeBufferedStill();
            byte[] array=new byte[8192];
            int t;
            while ((t=image_stream.read(array))!=-1){
                System.out.println(t);
                stream.write(array,0,t);
            }
            stream.write(-1);
            stream.flush();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

    }

}
