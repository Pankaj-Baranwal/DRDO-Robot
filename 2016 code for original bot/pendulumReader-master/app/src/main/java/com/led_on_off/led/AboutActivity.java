package com.led_on_off.led;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class AboutActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
    }
    public void web(View view) {
        Intent webIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/Pankaj-Baranwal"));
        startActivity(webIntent);
    }
}
