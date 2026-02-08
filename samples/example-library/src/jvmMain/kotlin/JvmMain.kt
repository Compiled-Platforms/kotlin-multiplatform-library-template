/**
 * JVM-specific entry point for the sample application.
 * 
 * This allows the sample to be run as a standard JVM application:
 * ./gradlew :samples:example-library:run
 */
fun main() {
    // Call the common main function from Main.kt
    com.compiledplatforms.kmp.library.fibonacci.main()
}
