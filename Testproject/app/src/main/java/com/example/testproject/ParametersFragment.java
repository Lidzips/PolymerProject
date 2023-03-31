package com.example.testproject;

import android.os.AsyncTask;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.testproject.databinding.FragmentParametersBinding;

import java.io.IOException;
import java.util.Arrays;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ParametersFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ParametersFragment extends Fragment {

    private FragmentParametersBinding binding;

    private ServerConnector serverConnector;
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public ParametersFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment ParametersFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static ParametersFragment newInstance(String param1, String param2) {
        ParametersFragment fragment = new ParametersFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        binding = FragmentParametersBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        binding.retrainBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Integer batch = Integer.parseInt(binding.batchText.getText().toString());
                Integer epochs = Integer.parseInt(binding.epochText.getText().toString());
                String numbers = binding.layerText.getText().toString();
                String[] numbersArray = numbers.split(" ");
                Integer[] layers = new Integer[numbersArray.length];
                for (int i = 0; i < numbersArray.length; i++) {
                    layers[i] = Integer.valueOf(numbersArray[i]);
                }

                RetrainNeuNetTask task = new RetrainNeuNetTask();
                task.execute(batch, epochs, layers[0]);
            }
        });
    }

    public class RetrainNeuNetTask extends AsyncTask<Integer, Void, Void> {

        @Override
        protected Void doInBackground(Integer... params) {
            Integer batch = params[0];
            Integer epochs = params[1];
            Integer[] layers = Arrays.copyOfRange(params, 2, params.length);

            try {
                ServerConnector.RetrainNeuNet(batch, epochs, layers);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            return null;
        }

    }


}