package com.google.android.gms.samples.vision.face.facetracker;

import android.app.Service;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

public class SoundService extends Service implements MediaPlayer.OnPreparedListener {

    private static final String TAG = "MyService";
    String url;
    MediaPlayer mp;

    public IBinder onBind(Intent intent) {

        Log.i("OnBind", "Inside OnBind");
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public void onCreate() {
        Toast.makeText(this, "My Service Created", Toast.LENGTH_LONG).show();
        Log.i(TAG, "onCreate");

        mp = new MediaPlayer();
        mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
    }

    @Override
    public void onDestroy() {
        Toast.makeText(this, "My Service Stopped", Toast.LENGTH_LONG).show();
        Log.d("Stopping", "onDestroy");

        mp.stop();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startid) {
        Toast.makeText(this, "My Service Started", Toast.LENGTH_LONG).show();
        Log.i("Starting", "onStart");

        url = intent.getExtras().getString("url");
        Log.i("Starting2", "onStart2");
        try {
            mp.reset();
            Log.i("URLIS",""+url);
            mp.setDataSource(url);
            Log.i("Starting3", "onStart3");
            mp.setOnPreparedListener(this);
            Log.i("Starting4", "onStart4");
            mp.prepareAsync();
            Log.i("Starting5", "onStart5");
        } catch(Exception e){}
        return START_STICKY;
    }

    @Override
    public void onPrepared(MediaPlayer mediaPlayer) {
        Log.i("Starting4", "onStart4");
        mediaPlayer.start();
    }
}