package com.example.mobile;

import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.chaquo.python.PyObject;

public class MainActivity extends FlutterActivity {
    private static final String CHANNEL = "chaquopy";

    @Override
    public void configureFlutterEngine(FlutterEngine flutterEngine) {
        super.configureFlutterEngine(flutterEngine);
        new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
            .setMethodCallHandler((call, result) -> {
                if (call.method.equals("generateBill")) {
                    String data = call.argument("data");
                    if (data == null) {
                        result.error("BAD_ARGUMENT", "data required", null);
                        return;
                    }
                    try {
                        // Initialize Python if not already started
                        if (!Python.isStarted()) {
                            Python.start(new AndroidPlatform(this));
                        }
                        // Load the Python module (bill_generator.py)
                        Python py = Python.getInstance();
                        PyObject module = py.getModule("bill_generator");
                        // Call the Python function with the input path
                        PyObject output = module.callAttr("generate_bill", data);
                        String outputPath = output.toString();
                        result.success(outputPath);
                    } catch (Exception e) {
                        result.error("PYTHON_ERROR", e.getMessage(), null);
                    }
                } else {
                    result.notImplemented();
                }
            });
    }
}
