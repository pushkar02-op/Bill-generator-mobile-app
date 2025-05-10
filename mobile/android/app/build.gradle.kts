plugins {
    id("com.android.application")
    id("kotlin-android")
    id("com.chaquo.python")
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.mobile"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        applicationId = "com.example.billgenerator"
        multiDexEnabled = true  // Enable Multidex

        minSdk = 24
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName

        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }

        // Corrected Chaquopy block
        
    }

    buildTypes {
        release {
            // Ensure the correct signing configuration is used
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    dependencies {
        // Adding Multidex support
        implementation("androidx.multidex:multidex:2.0.1")
    }
}
chaquopy {
    defaultConfig {
            pip {
                // Ensure these libraries are compatible with Chaquopy
                install("pandas")
                install("openpyxl")
            }
        }
}

flutter {
    source = "../.."
}
