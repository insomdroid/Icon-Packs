plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.insomdroid.iconpacks.nothink"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.insomdroid.iconpacks.nothink"
        minSdk = 29
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            // appfilter.xml stores drawable names as strings, so the resource shrinker
            // cannot see those references and would strip the mapped icon artwork.
            isShrinkResources = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
            // Build a signed release APK automatically without repository secrets.
            // GitHub-hosted runners use a fresh debug keystore, so signatures can differ between runs.
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation(project(":core"))
}
