# R8 Code Optimization

Each library in this monorepo includes R8 consumer rules to ensure proper code preservation when used in Android apps with code shrinking and optimization enabled.

## What is R8?

R8 is Android's modern code shrinker, optimizer, and obfuscator that replaced ProGuard. It:

- Removes unused code (tree shaking)
- Optimizes bytecode for better performance
- Obfuscates code to make reverse engineering harder
- Shrinks app size by removing unused resources

## Consumer Rules

Each library includes a `consumer-rules.pro` file with sensible defaults:

```pro
# Keep all public API classes and members
-keep public class com.compiledplatforms.kmp.library.** { *; }

# Keep Kotlin metadata for reflection
-keep class kotlin.Metadata { *; }

# Keep Kotlin coroutines (if used)
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}

# Keep generic signatures for reflection and serialization
-keepattributes Signature

# Keep source file names and line numbers for debugging
-keepattributes SourceFile,LineNumberTable
```

These rules are automatically applied when your library is consumed by an Android app.

## Customizing R8 Rules

When creating a new library, customize the `consumer-rules.pro` file based on your library's needs:

### For Libraries Using Reflection

```pro
# Keep classes accessed via reflection
-keep class com.compiledplatforms.kmp.library.yourlib.** { *; }

# Keep specific methods accessed via reflection
-keepclassmembers class com.compiledplatforms.kmp.library.yourlib.MyClass {
    public <methods>;
}
```

### For Libraries with Serialization (kotlinx.serialization)

```pro
# Keep serializers
-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}

-keepclasseswithmembers class kotlinx.serialization.json.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# Keep @Serializable classes
-keep,includedescriptorclasses class com.compiledplatforms.kmp.library.yourlib.**$$serializer { *; }
-keepclassmembers class com.compiledplatforms.kmp.library.yourlib.** {
    *** Companion;
}
```

### For Libraries with Data Classes Used as API Models

```pro
# Keep data classes with all fields
-keep class com.compiledplatforms.kmp.library.yourlib.models.** { *; }
```

### For Libraries with Native Methods

```pro
# Keep native methods
-keepclasseswithmembernames,includedescriptorclasses class * {
    native <methods>;
}
```

### For Libraries with Custom Views

```pro
# Keep custom views
-keep public class * extends android.view.View {
    public <init>(android.content.Context);
    public <init>(android.content.Context, android.util.AttributeSet);
    public <init>(android.content.Context, android.util.AttributeSet, int);
    public void set*(***);
}
```

## Testing R8 Rules

To verify your R8 rules work correctly:

### 1. Create a Test Android App

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}

dependencies {
    implementation("com.compiledplatforms.kmp.library:your-library:1.0.0")
}
```

### 2. Build and Test Release Build

```bash
./gradlew assembleRelease
./gradlew connectedAndroidTest
```

### 3. Analyze R8 Output

Check the R8 mapping file to see what was kept/removed:

```bash
cat app/build/outputs/mapping/release/mapping.txt
```

## R8 Full Mode

R8 has two modes:

### Compatibility Mode (Default)
- Behaves like ProGuard
- More conservative optimizations
- Better compatibility with older rules

### Full Mode (Recommended)
- More aggressive optimizations
- Better performance and smaller size
- May require updating rules

To enable R8 full mode in your test app:

```properties
# gradle.properties
android.enableR8.fullMode=true
```

## Common R8 Issues and Solutions

### Issue: ClassNotFoundException at Runtime

**Cause**: Class was removed by R8  
**Solution**: Add a `-keep` rule for the class

```pro
-keep class com.compiledplatforms.kmp.library.yourlib.MissingClass { *; }
```

### Issue: NoSuchMethodException at Runtime

**Cause**: Method was removed or renamed  
**Solution**: Keep the specific method

```pro
-keepclassmembers class com.compiledplatforms.kmp.library.yourlib.MyClass {
    public void myMethod(...);
}
```

### Issue: Reflection Not Working

**Cause**: Class names were obfuscated  
**Solution**: Keep class names for reflected classes

```pro
-keepnames class com.compiledplatforms.kmp.library.yourlib.** { *; }
```

### Issue: Serialization Failing

**Cause**: Serializer classes were removed  
**Solution**: Keep serialization-related classes

```pro
-keep class * implements kotlinx.serialization.KSerializer {
    public <methods>;
}
```

## Best Practices

1. **Start Minimal**: Only keep what's necessary for your public API
2. **Test Early**: Enable R8 in debug builds during development
3. **Use -keepnames Instead of -keep**: When you only need to preserve names, not prevent optimization
4. **Leverage -if Rules**: Conditionally keep classes based on usage
5. **Document Why**: Add comments explaining why each rule is needed
6. **Review Mapping Files**: Regularly check what's being kept/removed
7. **Keep Stack Traces Readable**: Always include `SourceFile` and `LineNumberTable` attributes

## R8-Specific Features

### Conditional Keep Rules

```pro
# Only keep Serializer if the class is used
-if class com.compiledplatforms.kmp.library.yourlib.MyModel
-keep class com.compiledplatforms.kmp.library.yourlib.MyModel$$serializer { *; }
```

### Assume No Side Effects

```pro
# Tell R8 these methods have no side effects
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}
```

## Resources

- [Android R8 Documentation](https://developer.android.com/studio/build/shrink-code)
- [R8 Full Mode](https://r8.googlesource.com/r8/+/refs/heads/master/compatibility-faq.md)
- [ProGuard/R8 Rule Syntax](https://www.guardsquare.com/manual/configuration/usage)
- [Kotlin R8 Guidelines](https://kotlinlang.org/docs/native-objc-interop.html#kotlin-r8)
