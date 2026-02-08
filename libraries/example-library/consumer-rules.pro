# Consumer rules for R8
# These rules are automatically applied when this library is used in an Android app

# Keep all public API classes and members
-keep public class com.compiledplatforms.kmp.library.** { *; }

# Keep Kotlin metadata for reflection
-keep class kotlin.Metadata { *; }

# Keep Kotlin coroutines (if used)
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembers class kotlinx.coroutines.** {
    volatile <fields>;
}

# Keep serialization annotations (if using kotlinx.serialization)
-keepattributes *Annotation*, InnerClasses
-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}
-keepclasseswithmembers class kotlinx.serialization.json.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# Keep generic signatures for reflection and serialization
-keepattributes Signature

# Keep source file names and line numbers for debugging
-keepattributes SourceFile,LineNumberTable

# R8 specific: Keep enum values
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# R8 specific: Keep Parcelable implementations (if used)
-keepclassmembers class * implements android.os.Parcelable {
    public static final ** CREATOR;
}
