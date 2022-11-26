package com.example.geofencing;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.http.GET;

public interface ZoneAPI {
    //http://127.0.0.1:5000/

    @GET("getZonesApp")
    Call<ArrayList<ZoneModel>> getAllZones();
}

