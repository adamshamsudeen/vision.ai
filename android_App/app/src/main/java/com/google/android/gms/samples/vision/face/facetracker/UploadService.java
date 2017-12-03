package com.google.android.gms.samples.vision.face.facetracker;

import android.app.Service;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.IBinder;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

public class UploadService extends Service {
    Bitmap bitmap3;
    public UploadService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }


    @Override
    public void onCreate() {
        Toast.makeText(this, "My Service Created", Toast.LENGTH_LONG).show();

    }

    @Override
    public void onDestroy() {
        Toast.makeText(this, "My Service Stopped", Toast.LENGTH_LONG).show();
        Log.d("Stopping", "onDestroy");

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startid) {
        Toast.makeText(this, "My Service Started", Toast.LENGTH_LONG).show();
        String myurl = intent.getExtras().getString("url");

        String uri = intent.getExtras().getString("uri");
        Uri uri1 = Uri.parse(uri);
        try {
            bitmap3 = MediaStore.Images.Media.getBitmap(this.getContentResolver(), uri1);
            int nh = (int) (bitmap3.getHeight() * (512.0 / bitmap3.getWidth()));
            bitmap3 = Bitmap.createScaledBitmap(bitmap3, 512, nh, true);
        }
        catch (Exception e){

        }
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        StringRequest stringRequest = new StringRequest(Request.Method.POST, myurl, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

                Toast.makeText(UploadService.this, ""+response, Toast.LENGTH_LONG).show();
                Log.i("Myresponse",""+response);
                Intent soundintent = new Intent(UploadService.this, SoundService.class);
                soundintent.putExtra("url",response);
                startService(soundintent);

//                Intent i = new Intent(MainActivity.this, SoundService.class);
//                i.putExtra("url",response);
//                startService(i);

                stopSelf();


            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("Mysmart",""+error);
                Toast.makeText(UploadService.this, "Error"+error, Toast.LENGTH_LONG).show();

                stopSelf();




            }
        })
        {

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> param = new HashMap<>();


                String images3 = getStringImage(bitmap3);
                param.put("image",images3);
                return param;
            }
        };

        stringRequest.setRetryPolicy(new DefaultRetryPolicy(
                90000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestQueue.add(stringRequest);
        return START_STICKY;


    }

    public String getStringImage(Bitmap bitmap){
        Log.i("MyHitesh",""+bitmap);
        ByteArrayOutputStream baos=new  ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG,100, baos);
        byte [] b=baos.toByteArray();
        String temp= Base64.encodeToString(b, Base64.DEFAULT);


        return temp;
    }




}
