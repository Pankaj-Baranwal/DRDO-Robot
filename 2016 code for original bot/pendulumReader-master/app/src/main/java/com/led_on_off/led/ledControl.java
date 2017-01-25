package com.led_on_off.led;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

import static com.led_on_off.led.R.id.etLength;


public class ledControl extends AppCompatActivity{

    //SPP UUID. Look for it
    static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    String address = null;
    BluetoothAdapter myBluetooth = null;
    BluetoothSocket btSocket = null;

    Button start;
    TextView output;
    EditText angle, distance;

    Handler workerThread;
    private ProgressDialog progress;
    private boolean isBtConnected = false;
    private ConnectedThread mConnectedThread;
    private Thread thread;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent newint = getIntent();
        address = newint.getStringExtra(DeviceList.EXTRA_ADDRESS); //receive the address of the
        // bluetooth device

        //view of the ledControl
        setContentView(R.layout.activity_led_control);

        //call the widgets
        start = (Button) findViewById(R.id.start);


        angle = (EditText) findViewById(etLength);
        distance = (EditText) findViewById(R.id.etRep);


        FloatingActionButton fabDiscnt = (FloatingActionButton) findViewById(R.id.discnt);

        assert fabDiscnt != null;
        fabDiscnt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Disconnect();
            }
        });

        new ConnectBT().execute(); //Call the class to connect

        //commands to be sent to bluetooth
        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!angle.getText().toString().trim().isEmpty() && !distance.getText().toString().trim().isEmpty()) {
                    startConversing();
                    mConnectedThread = new ConnectedThread(btSocket);
                    mConnectedThread.start();
                } else {
                    msg("Please enter all values");
                }
            }
           });

    }

    void beginListenForData() {


    }

    @Override
    protected void onPause() {
        super.onPause();

        if (thread != null) {
            thread.interrupt();
        }
        Disconnect();
    }

    private void Disconnect() {
        if (btSocket != null) //If the btSocket is busy
        {
            try {
                btSocket.close(); //close connection
            } catch (IOException e) {
                msg("Error");
            }
        }

        if (thread != null) {
            thread.interrupt();
        }

        finish(); //return to the first layout

    }


    private void startConversing() {
        if (btSocket != null) {
            try {
                btSocket.getOutputStream().write(("a"+angle.getText().toString()+"d"+distance.getText().toString()).getBytes());
                beginListenForData();
            } catch (IOException e) {
                msg("Error");
            }
        }
    }

    // fast way to call Toast
    private void msg(String s) {
        Toast.makeText(getApplicationContext(), s, Toast.LENGTH_LONG).show();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_led_control, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    private class ConnectBT extends AsyncTask<Void, Void, Void>  // UI thread
    {
        StringBuilder recDataString = new StringBuilder();
        private boolean ConnectSuccess = true; //if it's here, it's almost connected

        @Override
        protected void onPreExecute() {
            progress = ProgressDialog.show(ledControl.this, "Connecting...", "Please wait!!!");
            //show a progress dialog
        }

        @Override
        protected Void doInBackground(Void... devices) //while the progress dialog is shown, the
        // connection is done in background
        {
            try {
                if (btSocket == null || !isBtConnected) {
                    myBluetooth = BluetoothAdapter.getDefaultAdapter();//get the mobile bluetooth
                    // device
                    BluetoothDevice dispositivo = myBluetooth.getRemoteDevice(address);//connects
                    // to the device's address and checks if it's available
                    btSocket = dispositivo.createInsecureRfcommSocketToServiceRecord(myUUID);
                    //create a RFCOMM (SPP) connection
                    BluetoothAdapter.getDefaultAdapter().cancelDiscovery();
                    btSocket.connect();//start connection

                }
            } catch (IOException e) {
                ConnectSuccess = false;//if the try failed, you can check the exception here
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result) //after the doInBackground, it checks if
        // everything went fine
        {
            super.onPostExecute(result);

            if (!ConnectSuccess) {
                msg("Connection Failed. Is it SPP Bluetooth? Try again.");
                finish();
            } else {
                msg("Connected.");
                isBtConnected = true;

                workerThread = new Handler() {
                    public void handleMessage(android.os.Message msg) {
                        if (msg.what == 0) {
                            //if message is what we want
                            String readMessage = (String) msg.obj;

                            recDataString.append(readMessage);
                            //keep appending to string until ~
                            int endOfLineIndex = recDataString.indexOf("~");
                            // determine the end-of-line
                            if (endOfLineIndex > 0) {
                                // extract string
                                if (recDataString.indexOf("#") != -1 && recDataString.indexOf("~") != -1) {

                                    Log.e("TAG", "Data Received = " + recDataString.toString());

//                                    addEntry(recDataString.substring
//                                            (recDataString.indexOf("#") + 1, recDataString.indexOf
//                                                    ("~")));
                                    recDataString.delete(0, recDataString.length());
                                }
                            }
                        }
                    }
                };


            }
            progress.dismiss();
        }
    }

    private class ConnectedThread extends Thread {
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;

        //creation of the connect thread
        public ConnectedThread(BluetoothSocket socket) {
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            try {
                //Create I/O streams for connection
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {
            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
        }

        public void run() {
            byte[] buffer = new byte[256];
            int bytes;

            // Keep looping to listen for received messages
            while (true) {
                try {
                    bytes = mmInStream.read(buffer);            //read bytes from input buffer
                    String readMessage = new String(buffer, 0, bytes);
                    // Send the obtained bytes to the UI Activity via handler
                    workerThread.obtainMessage(0, bytes, -1, readMessage).sendToTarget();
                } catch (IOException e) {
                    break;
                }
            }
        }
    }
}