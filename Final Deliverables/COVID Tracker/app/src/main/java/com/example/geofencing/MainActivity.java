package com.example.geofencing;

import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.content.Intent;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.EditText;
import com.google.gson.Gson;
import android.widget.Toast;
import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);



        Button btn = (Button)findViewById(R.id.buttonLogin);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText username, password;
                username = (EditText) findViewById(R.id.inputUsernameLogin);
                String username2 = (String) username.getText().toString();

                password = (EditText) findViewById(R.id.inputPasswordLogin);
                String password2 = (String) password.getText().toString();

                Log.d("log", username2 + password2);
                if(password2.equals("jerry123") && username2.equals("jerry")) {
                    startActivity(new Intent(MainActivity.this, MapsActivity.class));
                    Toast.makeText(MainActivity.this, "Logging in", Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(MainActivity.this, "Incorrect username or password", Toast.LENGTH_LONG).show();
                }
            }
        });
    }
}
