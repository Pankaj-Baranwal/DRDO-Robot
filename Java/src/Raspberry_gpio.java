import com.pi4j.io.gpio.*;

/**
 * Created by karan on 28/1/17.
 */
public class Raspberry_gpio {
    GpioPinDigitalOutput pin[]=new GpioPinDigitalOutput[4];
    GpioPinDigitalInput status_pin;
    public Raspberry_gpio(){
        final GpioController gpio = GpioFactory.getInstance();
        pin[0]=gpio.provisionDigitalOutputPin(RaspiPin.GPIO_00,"1",PinState.LOW);
        pin[1]=gpio.provisionDigitalOutputPin(RaspiPin.GPIO_02,"1",PinState.LOW);
        pin[2]=gpio.provisionDigitalOutputPin(RaspiPin.GPIO_03,"1",PinState.LOW);
        pin[3]=gpio.provisionDigitalOutputPin(RaspiPin.GPIO_04,"1",PinState.LOW);
        status_pin=gpio.provisionDigitalInputPin(RaspiPin.GPIO_01);
    }

    public void wait_till_command_executed_on_firebird(){
        while (status_pin.isLow());
    }
    public void send_control_word(int control[]){

        for(int i=0;i<4;i++)
            if(control[i]==0) pin[i].low();
            else pin[i].high();

    }

}
