package com.example.thunderbolt.upload;

import com.example.thunderbolt.upload.ResultObject;

import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
public interface VideoInterface {
    @Multipart
    @POST("/upload")
    Call<ResultObject> uploadVideoToServer(@Part MultipartBody.Part video);
}