


//import com.pi4j.io.gpio.GpioController;
//import com.pi4j.io.gpio.GpioFactory;
//import com.pi4j.io.gpio.GpioPinDigitalOutput;
//import com.pi4j.io.gpio.PinState;
//import com.pi4j.io.gpio.RaspiPin;

import java.awt.image.BufferedImage;
import java.io.*;

/**
 * This example code demonstrates how to perform simple state
 * control of a GPIO pin on the Raspberry Pi.
 *
 * @author Robert Savage
 */
public class ControlGpioExample {

    public static void main(String[] args) throws InterruptedException, IOException, FailedToRunRaspistillException {

        System.out.println("<--Pi4J--> GPIO Control Example ... started.");

        RPiCamera piCamera = new RPiCamera("/home/karan/Pictures");
        InputStream image = piCamera.takeBufferedStill();
        FileOutputStream stream=new FileOutputStream(new File("temp.jpg"));
        byte[] buffer = new byte[1024];
        int len;
        while ((len = image.read(buffer)) != -1) {
            stream.write(buffer, 0, len);
        }
        stream.flush();
        stream.close();
        image.close();
//
//        // create gpio controller
//        final GpioController gpio = GpioFactory.getInstance();
//
//        // provision gpio pin #01 as an output pin and turn on
//        final GpioPinDigitalOutput pin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_01, "MyLED", PinState.HIGH);
//
//        // set shutdown state for this pin
//        pin.setShutdownOptions(true, PinState.LOW);
//
//        System.out.println("--> GPIO state should be: ON");
//
//        Thread.sleep(5000);
//
//        // turn off gpio pin #01
//        pin.low();
//        System.out.println("--> GPIO state should be: OFF");
//
//        Thread.sleep(5000);
//
//        // toggle the current state of gpio pin #01 (should turn on)
//        pin.toggle();
//        System.out.println("--> GPIO state should be: ON");
//
//        Thread.sleep(5000);
//
//        // toggle the current state of gpio pin #01  (should turn off)
//        pin.toggle();
//        System.out.println("--> GPIO state should be: OFF");
//
//        Thread.sleep(5000);
//
//        // turn on gpio pin #01 for 1 second and then off
//        System.out.println("--> GPIO state should be: ON for only 1 second");
//        pin.pulse(1000, true); // set second argument to 'true' use a blocking call
//
//        // stop all GPIO activity/threads by shutting down the GPIO controller
//        // (this method will forcefully shutdown all GPIO monitoring threads and scheduled tasks)
//        gpio.shutdown();
//
//        System.out.println("Exiting ControlGpioExample");
//    }
    }
}