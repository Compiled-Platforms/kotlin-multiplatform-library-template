# Testing Kotlin Multiplatform Libraries

This template provides a comprehensive testing setup for Kotlin Multiplatform libraries with best-in-class tools.

## Testing Stack

The template includes:

- ✅ **kotlin.test** - Standard testing framework (works everywhere)
- ✅ **kotlinx-coroutines-test** - Testing coroutines and suspend functions
- ✅ **Turbine** - Simple and powerful Flow testing
- ✅ **Mokkery** - Modern KMP mocking library (when you need mocks)
- ✅ **Kover** - Code coverage tracking

## Quick Start

### Basic Test

```kotlin
import kotlin.test.Test
import kotlin.test.assertEquals

class MyLibraryTest {
    @Test
    fun testBasicFunction() {
        val result = myFunction(5)
        assertEquals(10, result)
    }
}
```

### Testing Suspend Functions

```kotlin
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class CoroutineTest {
    @Test
    fun testSuspendFunction() = runTest {
        val result = fetchDataAsync()
        assertEquals("data", result)
    }
}
```

### Testing Flows

```kotlin
import app.cash.turbine.test
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class FlowTest {
    @Test
    fun testFlow() = runTest {
        myFlow().test {
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            awaitComplete()
        }
    }
}
```

## kotlin.test

**kotlin.test** is the standard Kotlin testing library that works across all platforms.

### Assertions

```kotlin
import kotlin.test.*

@Test
fun testAssertions() {
    // Equality
    assertEquals(expected, actual)
    assertNotEquals(illegal, actual)
    
    // Boolean
    assertTrue(condition)
    assertFalse(condition)
    
    // Nullability
    assertNull(value)
    assertNotNull(value)
    
    // Exceptions
    assertFailsWith<IllegalArgumentException> {
        throwError()
    }
    
    // Custom message
    assertEquals(expected, actual, "Custom failure message")
}
```

### Test Lifecycle

```kotlin
class LifecycleTest {
    @BeforeTest
    fun setup() {
        // Runs before each test
    }
    
    @AfterTest
    fun teardown() {
        // Runs after each test
    }
    
    @Test
    fun test1() { }
    
    @Test
    fun test2() { }
}
```

### Ignoring Tests

```kotlin
@Ignore("Not implemented yet")
@Test
fun futureTest() {
    // This test won't run
}
```

## kotlinx-coroutines-test

**kotlinx-coroutines-test** provides utilities for testing coroutines with virtual time.

### runTest

`runTest` creates a test coroutine scope with virtual time:

```kotlin
@Test
fun testWithRunTest() = runTest {
    // Can call suspend functions directly
    val result = suspendFunction()
    assertEquals(expected, result)
}
```

### Virtual Time

Delays are skipped automatically in virtual time:

```kotlin
@Test
fun testDelay() = runTest {
    val startTime = currentTime
    
    delay(1000) // Executes instantly in virtual time
    
    val endTime = currentTime
    assertEquals(1000, endTime - startTime) // Time advanced by 1000ms
}
```

**Real time:** This test runs in ~1 second  
**Virtual time:** This test runs instantly

### Testing Timing

```kotlin
@Test
fun testTiming() = runTest {
    val job = launch {
        delay(100)
        doSomething()
    }
    
    // Advance time manually if needed
    advanceTimeBy(50)
    // doSomething() hasn't run yet
    
    advanceTimeBy(50)
    // Now doSomething() has run
    
    job.join()
}
```

### Testing Dispatchers

```kotlin
@Test
fun testWithDispatchers() = runTest {
    // StandardTestDispatcher is used by default
    val result = withContext(Dispatchers.Default) {
        // Runs on test dispatcher
        computeValue()
    }
    assertEquals(expected, result)
}
```

### UnconfinedTestDispatcher

For immediate execution without virtual time:

```kotlin
@Test
fun testUnconfined() = runTest(UnconfinedTestDispatcher()) {
    // Coroutines execute immediately
    launch {
        // Runs immediately, no delay
        doSomething()
    }
    // doSomething() has already executed
}
```

## Turbine

**Turbine** makes Flow testing simple and readable.

### Basic Flow Testing

```kotlin
@Test
fun testFlow() = runTest {
    myFlow().test {
        // Assert each emission
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())
        assertEquals(3, awaitItem())
        
        // Assert completion
        awaitComplete()
    }
}
```

### Skipping Items

```kotlin
@Test
fun testSkip() = runTest {
    myFlow().test {
        // Skip first 2 items
        skipItems(2)
        
        // Test remaining items
        assertEquals(3, awaitItem())
        awaitComplete()
    }
}
```

### Testing Errors

```kotlin
@Test
fun testError() = runTest {
    errorFlow().test {
        assertEquals(1, awaitItem())
        
        // Assert error
        val error = awaitError()
        assertTrue(error is IllegalStateException)
        assertEquals("Error message", error.message)
    }
}
```

### Testing Cancellation

```kotlin
@Test
fun testCancellation() = runTest {
    infiniteFlow().test {
        // Take some items
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())
        
        // Cancel the flow
        cancel()
    }
}
```

### Expecting No Events

```kotlin
@Test
fun testNoEvents() = runTest {
    emptyFlow<Int>().test {
        // Assert no items were emitted
        awaitComplete()
    }
}
```

### Testing with Timeout

```kotlin
@Test
fun testTimeout() = runTest {
    slowFlow().test(timeout = 5.seconds) {
        // Fail if flow doesn't complete within 5 seconds
        awaitItem()
        awaitComplete()
    }
}
```

### Collecting All Items

```kotlin
@Test
fun testCollectAll() = runTest {
    val items = myFlow().test {
        // Collect all items until completion
        awaitComplete()
    }.items
    
    assertEquals(listOf(1, 2, 3), items)
}
```

## Testing Patterns

### Testing State Flows

```kotlin
class StateFlowTest {
    private val _state = MutableStateFlow(0)
    val state: StateFlow<Int> = _state.asStateFlow()
    
    @Test
    fun testStateFlow() = runTest {
        state.test {
            // StateFlow immediately emits current value
            assertEquals(0, awaitItem())
            
            _state.value = 1
            assertEquals(1, awaitItem())
            
            _state.value = 2
            assertEquals(2, awaitItem())
            
            cancel()
        }
    }
}
```

### Testing Shared Flows

```kotlin
class SharedFlowTest {
    private val _events = MutableSharedFlow<String>()
    val events: SharedFlow<String> = _events.asSharedFlow()
    
    @Test
    fun testSharedFlow() = runTest {
        events.test {
            _events.emit("event1")
            assertEquals("event1", awaitItem())
            
            _events.emit("event2")
            assertEquals("event2", awaitItem())
            
            cancel()
        }
    }
}
```

### Testing Cold Flows

```kotlin
@Test
fun testColdFlow() = runTest {
    val coldFlow = flow {
        emit(1)
        delay(100)
        emit(2)
    }
    
    // Each collection starts from the beginning
    coldFlow.test {
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())
        awaitComplete()
    }
    
    // Second collection also starts from beginning
    coldFlow.test {
        assertEquals(1, awaitItem())
        assertEquals(2, awaitItem())
        awaitComplete()
    }
}
```

### Testing Hot Flows

```kotlin
@Test
fun testHotFlow() = runTest {
    val hotFlow = MutableSharedFlow<Int>()
    
    // Start collecting before emissions
    hotFlow.test {
        hotFlow.emit(1)
        assertEquals(1, awaitItem())
        
        hotFlow.emit(2)
        assertEquals(2, awaitItem())
        
        cancel()
    }
}
```

## Mokkery (Mocking)

**Mokkery** is a modern Kotlin Multiplatform mocking library that uses KSP for code generation.

### When to Use Mokkery

Use Mokkery when:
- ❌ Interface has many methods (fake would be too large)
- ❌ Need to verify specific interactions
- ❌ Testing third-party APIs you don't control
- ❌ Need to verify call order or count

### Basic Usage

```kotlin
import dev.mokkery.answering.returns
import dev.mokkery.everySuspend
import dev.mokkery.mock
import dev.mokkery.verifySuspend

@Test
fun testWithMock() = runTest {
    // Create mock
    val repository = mock<UserRepository>()
    
    // Setup behavior
    everySuspend { repository.getUser("123") } returns User("test")
    
    // Use mock
    val result = repository.getUser("123")
    
    // Verify
    assertEquals(User("test"), result)
    verifySuspend { repository.getUser("123") }
}
```

### Mocking Suspend Functions

```kotlin
@Test
fun testSuspendMocking() = runTest {
    val api = mock<ApiService>()
    
    // Use everySuspend for suspend functions
    everySuspend { api.fetchData(any()) } returns "data"
    
    val result = api.fetchData("id")
    assertEquals("data", result)
}
```

### Mocking Regular Functions

```kotlin
@Test
fun testRegularMocking() {
    val cache = mock<Cache>()
    
    // Use every for regular functions
    every { cache.get("key") } returns "value"
    
    val result = cache.get("key")
    assertEquals("value", result)
}
```

### Mocking Exceptions

```kotlin
@Test
fun testException() = runTest {
    val api = mock<ApiService>()
    
    everySuspend { 
        api.fetchData("error") 
    } throws IOException("Network error")
    
    assertFailsWith<IOException> {
        api.fetchData("error")
    }
}
```

### Verifying Interactions

```kotlin
@Test
fun testVerification() = runTest {
    val repository = mock<Repository>()
    everySuspend { repository.save(any()) } returns Unit
    
    repository.save("data1")
    repository.save("data2")
    
    // Verify call count
    verifySuspend(exactly = 2) { repository.save(any()) }
    
    // Verify specific call
    verifySuspend(exactly = 1) { repository.save("data1") }
    
    // Verify no calls
    verifySuspend(exactly = 0) { repository.delete(any()) }
}
```

### Argument Matchers

```kotlin
@Test
fun testMatchers() = runTest {
    val api = mock<ApiService>()
    
    // Match any argument
    everySuspend { api.fetchUser(any()) } returns User("default")
    
    // Match specific value
    everySuspend { api.fetchUser("admin") } returns User("admin")
    
    assertEquals(User("default"), api.fetchUser("user1"))
    assertEquals(User("admin"), api.fetchUser("admin"))
}
```

### Sequential Returns

```kotlin
@Test
fun testSequentialReturns() = runTest {
    val counter = mock<Counter>()
    
    // Return different values on each call
    everySuspend { counter.next() } returns 1 returns 2 returns 3
    
    assertEquals(1, counter.next())
    assertEquals(2, counter.next())
    assertEquals(3, counter.next())
}
```

## Manual Fakes vs. Mocking

For most library testing, **manual fakes** are simpler and more maintainable than mocking frameworks.

### Manual Fake (Recommended)

```kotlin
// Production interface
interface DataRepository {
    suspend fun getData(): String
    suspend fun saveData(data: String)
}

// Test fake
class FakeDataRepository : DataRepository {
    val savedData = mutableListOf<String>()
    var dataToReturn = "test-data"
    
    override suspend fun getData(): String = dataToReturn
    
    override suspend fun saveData(data: String) {
        savedData.add(data)
    }
}

// Test
@Test
fun testWithFake() = runTest {
    val repository = FakeDataRepository()
    repository.dataToReturn = "custom-data"
    
    val result = repository.getData()
    assertEquals("custom-data", result)
    
    repository.saveData("new-data")
    assertEquals(listOf("new-data"), repository.savedData)
}
```

**Advantages:**
- ✅ Simple and explicit
- ✅ No magic or reflection
- ✅ Works on all platforms
- ✅ Easy to debug
- ✅ Type-safe

### When to Use Mocking

Use mocking frameworks (Mokkery is included in this template) when:
- ❌ Interface has many methods (fake would be too large)
- ❌ Need to verify specific interactions
- ❌ Testing third-party APIs you don't control
- ❌ Testing legacy code with complex dependencies

## Platform-Specific Tests

### Common Tests (All Platforms)

```kotlin
// src/commonTest/kotlin/MyTest.kt
class MyTest {
    @Test
    fun testCommon() {
        // Runs on all platforms
    }
}
```

### JVM-Specific Tests

```kotlin
// src/jvmTest/kotlin/JvmTest.kt
class JvmTest {
    @Test
    fun testJvmSpecific() {
        // Only runs on JVM
        // Can use JVM-specific APIs
    }
}
```

### Android-Specific Tests

```kotlin
// src/androidHostTest/kotlin/AndroidTest.kt
class AndroidTest {
    @Test
    fun testAndroidSpecific() {
        // Only runs on Android
    }
}
```

### iOS-Specific Tests

```kotlin
// src/iosTest/kotlin/IosTest.kt
class IosTest {
    @Test
    fun testIosSpecific() {
        // Only runs on iOS
    }
}
```

## Best Practices

### 1. Test Behavior, Not Implementation

```kotlin
// Bad: Testing implementation details
@Test
fun testInternalState() {
    val obj = MyClass()
    assertEquals(0, obj.internalCounter) // Don't test private state
}

// Good: Testing behavior
@Test
fun testBehavior() {
    val obj = MyClass()
    val result = obj.doSomething()
    assertEquals(expected, result) // Test public API
}
```

### 2. One Assertion Per Test (When Possible)

```kotlin
// Bad: Multiple unrelated assertions
@Test
fun testEverything() {
    assertEquals(1, add(0, 1))
    assertEquals(5, multiply(2, 3)) // Unrelated
    assertEquals("hello", greet()) // Unrelated
}

// Good: Focused tests
@Test
fun testAdd() {
    assertEquals(1, add(0, 1))
}

@Test
fun testMultiply() {
    assertEquals(6, multiply(2, 3))
}
```

### 3. Use Descriptive Test Names

```kotlin
// Bad
@Test
fun test1() { }

// Good
@Test
fun `when user is logged out, returns null`() { }

// Also good
@Test
fun returnsNullWhenUserIsLoggedOut() { }
```

### 4. Arrange-Act-Assert Pattern

```kotlin
@Test
fun testWithPattern() {
    // Arrange: Set up test data
    val repository = FakeRepository()
    val useCase = MyUseCase(repository)
    
    // Act: Execute the behavior
    val result = useCase.execute()
    
    // Assert: Verify the outcome
    assertEquals(expected, result)
}
```

### 5. Test Edge Cases

```kotlin
@Test
fun testEmptyList() {
    assertEquals(0, sum(emptyList()))
}

@Test
fun testNegativeNumbers() {
    assertEquals(-5, sum(listOf(-2, -3)))
}

@Test
fun testLargeNumbers() {
    assertEquals(Long.MAX_VALUE, sum(listOf(Long.MAX_VALUE)))
}
```

### 6. Use runTest for All Coroutine Tests

```kotlin
// Bad: Using runBlocking in tests
@Test
fun badTest() = runBlocking {
    delay(1000) // Takes 1 real second
}

// Good: Using runTest
@Test
fun goodTest() = runTest {
    delay(1000) // Executes instantly with virtual time
}
```

## Running Tests

### Run All Tests

```bash
./gradlew test
```

### Run Tests for Specific Platform

```bash
./gradlew jvmTest           # JVM only
./gradlew testAndroid       # Android only
./gradlew iosSimulatorArm64Test  # iOS Simulator
./gradlew linuxX64Test      # Linux
```

### Run Tests for Specific Library

```bash
./gradlew :libraries:example-library:test
```

### Run Tests with Coverage

```bash
./gradlew test koverHtmlReport
```

### Run Tests in Watch Mode

```bash
./gradlew test --continuous
```

## Debugging Tests

### Print Debugging

```kotlin
@Test
fun debugTest() = runTest {
    val value = computeValue()
    println("Debug: value = $value") // Shows in test output
    assertEquals(expected, value)
}
```

### Breakpoints

Set breakpoints in your IDE and run tests in debug mode:
- IntelliJ/Android Studio: Right-click test → "Debug"
- Click in the gutter to set breakpoints

### Test Timeouts

```kotlin
@Test(timeout = 5000) // Timeout after 5 seconds
fun longRunningTest() {
    // Test that might hang
}
```

## Common Testing Mistakes

### ❌ Not Using runTest

```kotlin
// Wrong: No runTest
@Test
fun badTest() {
    val result = suspendFunction() // Compilation error!
}

// Correct
@Test
fun goodTest() = runTest {
    val result = suspendFunction() // Works!
}
```

### ❌ Not Awaiting Flow Completion

```kotlin
// Wrong: Flow might not complete
@Test
fun badFlowTest() = runTest {
    myFlow().test {
        assertEquals(1, awaitItem())
        // Missing awaitComplete()!
    }
}

// Correct
@Test
fun goodFlowTest() = runTest {
    myFlow().test {
        assertEquals(1, awaitItem())
        awaitComplete() // Always await completion or error
    }
}
```

### ❌ Testing Too Much in One Test

```kotlin
// Wrong: Testing multiple unrelated things
@Test
fun testEverything() {
    testFeature1()
    testFeature2()
    testFeature3()
}

// Correct: Separate tests
@Test
fun testFeature1() { }

@Test
fun testFeature2() { }

@Test
fun testFeature3() { }
```

## Additional Tools

### Kotest (Optional)

For more expressive assertions and BDD-style tests:

```kotlin
// Add to commonTest dependencies
implementation("io.kotest:kotest-assertions-core:5.8.0")

// Usage
@Test
fun testWithKotest() {
    result shouldBe expected
    list shouldContain item
    value.shouldBeGreaterThan(0)
}
```

### Example: Testing with Mokkery

```kotlin
interface DataRepository {
    suspend fun fetchData(id: String): String
    suspend fun saveData(id: String, data: String)
    // ... many more methods
}

@Test
fun testWithMokkery() = runTest {
    val repository = mock<DataRepository>()
    
    everySuspend { repository.fetchData("123") } returns "mocked-data"
    
    val result = repository.fetchData("123")
    assertEquals("mocked-data", result)
    
    verifySuspend { repository.fetchData("123") }
}
```

## Resources

- [kotlin.test Documentation](https://kotlinlang.org/api/latest/kotlin.test/)
- [kotlinx-coroutines-test Guide](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [Turbine GitHub](https://github.com/cashapp/turbine)
- [Mokkery Documentation](https://mokkery.dev/)
- [Kotest](https://kotest.io/)

## Quick Reference

```bash
# Run all tests
./gradlew test

# Run with coverage
./gradlew test koverHtmlReport

# Run specific platform
./gradlew jvmTest

# Run continuously
./gradlew test --continuous

# Run specific test
./gradlew test --tests "MyTest.testFunction"
```

**Golden Rule:** Write tests that are easy to read, easy to maintain, and test behavior, not implementation!
