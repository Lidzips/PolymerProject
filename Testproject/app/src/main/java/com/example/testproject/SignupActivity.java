package com.example.testproject;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;

import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.example.testproject.databinding.ActivitySignupBinding;

import java.io.IOException;
import java.time.Duration;
import java.util.Arrays;

public class SignupActivity extends AppCompatActivity {

    static Boolean response = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        Button create = findViewById(R.id.create_btn);
        create.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                EditText login = findViewById(R.id.text_login);
                EditText password = findViewById(R.id.text_password);
                EditText password2 = findViewById(R.id.text_password1);
                TextView error = findViewById(R.id.text_error);
                error.setText("");

                String loginText = login.getText().toString();
                String passwordText = password.getText().toString();
                String password2Text = password2.getText().toString();

                if (!passwordText.equals(password2Text)) {
                    error.setText("Password mismatch");
                    return;
                }

                SignUpUser task = new SignUpUser();
                task.execute(loginText, passwordText);

                if (response) {
                    Toast.makeText(SignupActivity.this, "Account created successfully", Toast.LENGTH_LONG).show();
                    Intent intent = new Intent(SignupActivity.this, LoginActivity.class);
                    startActivity(intent);
                } else {
                    error.setText("Error on creating user");
                }
            }
        });

        Button back = findViewById(R.id.back_btn);
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(SignupActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });
    }

    public class SignUpUser extends AsyncTask<String, Void, Boolean> {

        @Override
        protected Boolean doInBackground(String... params) {
            String login = params[0];
            String password = params[1];

            try {
                return ServerConnector.CreateAccount(login, password);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        protected void onPostExecute(Boolean response1) {
            response = response1;
        }

    }

}