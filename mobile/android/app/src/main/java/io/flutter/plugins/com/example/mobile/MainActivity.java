package com.example.mobile;

import android.content.Context;
import androidx.multidex.MultiDex;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.chaquo.python.PyObject;

public class MainActivity extends FlutterActivity {
    private static final String CHANNEL = "chaquopy";

    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        // Enable multidex for large apps
        MultiDex.install(this);
    }

    @Override
    public void configureFlutterEngine(FlutterEngine flutterEngine) {
        super.configureFlutterEngine(flutterEngine);

        // Initialize Python runtime once
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        // Pre-load your module
        PyObject module = Python.getInstance().getModule("bill_generator");

        new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
          .setMethodCallHandler((call, result) -> {
            if ("generateBill".equals(call.method)) {
                String inputPath = call.argument("data");
                String place     = call.argument("place");
                if (inputPath == null || place == null) {
                    result.error("BAD_ARGS", "Both 'data' and 'place' must be provided", null);
                    return;
                }
                try {
                    // Call your Python function
                    PyObject output = module.callAttr("generate_bill", inputPath, place);
                    result.success(output.toString());
                } catch (Exception e) {
                    result.error("PY_ERROR", e.getMessage(), null);
                }
            } else {
                result.notImplemented();
            }
          });
    }
}
