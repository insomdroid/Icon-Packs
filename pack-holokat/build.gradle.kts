plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }

val releaseStoreFile = System.getenv("HOLOKAT_RELEASE_STORE_FILE")
val releaseStorePassword = System.getenv("HOLOKAT_RELEASE_STORE_PASSWORD")
val releaseKeyAlias = System.getenv("HOLOKAT_RELEASE_KEY_ALIAS")
val releaseKeyPassword = System.getenv("HOLOKAT_RELEASE_KEY_PASSWORD")
val hasReleaseSigning = listOf(releaseStoreFile, releaseStorePassword, releaseKeyAlias, releaseKeyPassword).all { !it.isNullOrBlank() }

android {
    namespace = "com.insomdroid.iconpacks.holokat"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.insomdroid.iconpacks.holokat"
        minSdk = 29
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }
    signingConfigs {
        if (hasReleaseSigning) {
            create("temporaryRelease") {
                storeFile = file(requireNotNull(releaseStoreFile))
                storePassword = requireNotNull(releaseStorePassword)
                keyAlias = requireNotNull(releaseKeyAlias)
                keyPassword = requireNotNull(releaseKeyPassword)
            }
        }
    }
    buildTypes {
        getByName("release") {
            if (hasReleaseSigning) signingConfig = signingConfigs.getByName("temporaryRelease")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}
dependencies { implementation(project(":core")) }
