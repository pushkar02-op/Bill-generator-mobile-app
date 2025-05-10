package com.example.mobile;

import android.content.Context;
import androidx.multidex.MultiDex;
import com.chaquo.python.android.PyApplication;

/**
 * Combines Chaquopy’s PyApplication with AndroidX Multidex support.
 */
public class MainApplication extends PyApplication {
    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        MultiDex.install(this);
    }
}
