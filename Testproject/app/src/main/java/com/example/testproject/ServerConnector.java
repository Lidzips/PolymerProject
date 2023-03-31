package com.example.testproject;

import android.os.Build;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.Base64;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.nio.file.Paths;

public class ServerConnector {

    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;

    static String ip = "192.168.100.46";
    static int port = 8080;

    public void startConnection() throws IOException {
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    }

    public String sendMessage(String msg) throws IOException {
        out.println(msg);
        String resp = in.readLine();
        return resp;
    }

    public void stopConnection() throws IOException {
        in.close();
        out.close();
        clientSocket.close();
    }


    public static void TestConnection() {

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String string1 = "test";
        byte[] call1 = string1.getBytes(StandardCharsets.UTF_8);
        String response1 = null;
        try {
            response1 = conn.sendMessage(string1);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println(response1 + " " + response1.getClass().getName() + response1.length());
        System.out.println(string1 + " " + string1.getClass().getName() + string1.length());
        if (response1.equals(string1))
            System.out.println("Action confirmation received successfully");

        String string2 = "test";
        byte[] call2 = string2.getBytes(StandardCharsets.UTF_8);
        String response2 = null;
        try {
            response2 = conn.sendMessage(string2);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response2 == string2)
            System.out.println("2nd response received successfully");
    }

    public static void RetrainNeuNet(Integer batch, Integer epochs, Integer[] layers) throws IOException {

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection(); //insert host ipv4
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String action = "admin_retrain_neunet";
        String response = null;
        try {
            response = conn.sendMessage(action);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response.equals(action))
            System.out.println("Action confirmation received successfully");

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(batch));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response.equals("Batch value received"))
            System.out.println("Batch value sent successfully");

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(epochs));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response.equals("Epoch value received"))
            System.out.println("Epoch value sent successfully");

        String layersString = Arrays.toString(layers);
        response = null;
        try {
            response = conn.sendMessage(String.valueOf(layersString));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //if (response.equals("Layer values received"))
        //    System.out.println("Layer values sent successfully");


        if (response.equals("NeuNet retrained successfully"))
            System.out.println("Layer values sent successfully and NeuNet retrained successfully");

        conn.stopConnection();
    }

    public static Boolean CreateAccount(String login, String password) throws IOException {

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection(); //insert host ipv4
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String action = "new_acct";
        String response = null;
        try {
            response = conn.sendMessage(action);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(login));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response.equals("Login value received"))
            System.out.println("Login value sent successfully");

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(password));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        Boolean result = null;
        if (response.equals("Login taken")) {
            System.out.println("Password value sent successfully, user creation FAILED");
            result = false;
        } else if (response.equals("User created")) {
            System.out.println("Password value sent successfully, user creation SUCCESS");
            result = true;
        }
        conn.stopConnection();

        return result;
    }

    public static String Login(String login, String password) throws IOException { //returns FAILED , USER , ADMIN as str

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection(); //insert host ipv4
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String action = "login";
        String response = null;
        try {
            response = conn.sendMessage(action);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(login));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        if (response.equals("Login value received"))
            System.out.println("Login value sent successfully");

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(password));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        String result = null;
        if (response.equals("No match")) {
            System.out.println("Password value sent successfully, login FAILED");
            result = "FAIL";
        } else if (response.equals("User")) {
            System.out.println("Password value sent successfully, login USER");
            result = "USER";
        } else if (response.equals("Admin")) {
            System.out.println("Password value sent successfully, login ADMIN");
            result = "ADMIN";
        }

        conn.stopConnection();

        return result;
    }

    public static Integer NeuNetPredict(byte[] fileContent) throws IOException {

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection(); //insert host ipv4
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String action = "predict";
        String response = null;
        try {
            response = conn.sendMessage(action);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

       // File fi = new File(img_path);
        //byte[] fileContent = Files.readAllBytes(fi.toPath());
        String encodedImage = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            encodedImage = Base64.getEncoder().encodeToString(fileContent);
        }


        response = null;
        try {
            response = conn.sendMessage(encodedImage);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        Integer prediction = Integer.parseInt(response);

        conn.stopConnection();

        return prediction;
    }

    public static String UserHistory(String login) throws IOException {

        ServerConnector conn = new ServerConnector();

        try {
            conn.startConnection(); //insert host ipv4
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String action = "user_db_summary";
        String response = null;
        try {
            response = conn.sendMessage(action);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        response = null;
        try {
            response = conn.sendMessage(String.valueOf(login));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        conn.stopConnection();

        return response;
    }


}
