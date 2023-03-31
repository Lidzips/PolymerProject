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

import com.example.testproject.databinding.ActivityLoginBinding;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

public class LoginActivity extends AppCompatActivity {

    String response = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Button logIn = findViewById(R.id.login_btn);
        logIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                EditText login = findViewById(R.id.text_login);
                EditText password = findViewById(R.id.text_password);
                String loginText = login.getText().toString();
                String passwordText = password.getText().toString();
                TextView error = findViewById(R.id.text_error);
                error.setText("");

                SignInUser task = new SignInUser();
                task.execute(loginText, passwordText);

                String result = "";
                try {
                    result = task.get();
                } catch (InterruptedException | ExecutionException e) {
                    e.printStackTrace();
                }

                if (result.equals("ADMIN")) {
                    Intent intent = new Intent(LoginActivity.this, AdminActivity.class);
                    startActivity(intent);
                } else if (result.equals("USER")) {
                    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                    startActivity(intent);
                } else if (result.equals("FAILED")) {
                    error.setText("Login or password is incorrect");
                } else {
                    error.setText("Something went wrong");
                    System.out.println("123123" + result + "123123");
                }
            }
        });

        Button signUp = findViewById(R.id.signup_btn);
        signUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(LoginActivity.this, SignupActivity.class);
                startActivity(intent);
            }
        });
    }

    public class SignInUser extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String login = params[0];
            String password = params[1];

            try {
                return ServerConnector.Login(login, password);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            response = result;
        }

    }
}