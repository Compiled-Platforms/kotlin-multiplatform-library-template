package com.compiledplatforms.kmp.library.fibonacci

import dev.mokkery.answering.returns
import dev.mokkery.answering.throws
import dev.mokkery.everySuspend
import dev.mokkery.matcher.any
import dev.mokkery.mock
import dev.mokkery.verify
import dev.mokkery.verifySuspend
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/**
 * Example tests demonstrating Mokkery usage for mocking.
 * 
 * Mokkery is a modern KMP mocking library that uses KSP for code generation.
 * Use mocks when:
 * - Interface has many methods (fake would be too large)
 * - You need to verify specific interactions
 * - Testing third-party APIs you don't control
 * 
 * For simple interfaces, prefer manual fakes (see FibonacciRepository example).
 */
class MokkeryExampleTest {

    // Example interface that might be too complex for a manual fake
    interface ComplexDataSource {
        suspend fun fetchData(id: String): String
        suspend fun saveData(id: String, data: String)
        suspend fun deleteData(id: String)
        suspend fun listAll(): List<String>
        suspend fun count(): Int
        suspend fun clear()
        // Imagine 10+ more methods...
    }

    @Test
    fun testBasicMocking() = runTest {
        // Create a mock
        val dataSource = mock<ComplexDataSource>()
        
        // Setup behavior
        everySuspend { dataSource.fetchData("123") } returns "test-data"
        
        // Use the mock
        val result = dataSource.fetchData("123")
        
        // Verify result
        assertEquals("test-data", result)
        
        // Verify interaction
        verifySuspend { dataSource.fetchData("123") }
    }

    @Test
    fun testMockingWithAnyMatcher() = runTest {
        val dataSource = mock<ComplexDataSource>()
        
        // Match any argument
        everySuspend { dataSource.fetchData(any()) } returns "default-data"
        
        val result1 = dataSource.fetchData("123")
        val result2 = dataSource.fetchData("456")
        
        assertEquals("default-data", result1)
        assertEquals("default-data", result2)
    }

    @Test
    fun testMockingWithException() = runTest {
        val dataSource = mock<ComplexDataSource>()
        
        // Mock to throw exception
        everySuspend { 
            dataSource.fetchData("error") 
        } throws IllegalStateException("Not found")
        
        // Test error handling
        val result = try {
            dataSource.fetchData("error")
            "success"
        } catch (e: IllegalStateException) {
            "error: ${e.message}"
        }
        
        assertEquals("error: Not found", result)
    }

    @Test
    fun testMultipleCalls() = runTest {
        val dataSource = mock<ComplexDataSource>()
        
        everySuspend { dataSource.saveData(any(), any()) } returns Unit
        
        // Make multiple calls
        dataSource.saveData("1", "data1")
        dataSource.saveData("2", "data2")
        
        // Verify calls happened
        verifySuspend { dataSource.saveData("1", "data1") }
        verifySuspend { dataSource.saveData("2", "data2") }
    }

    @Test
    fun testDifferentReturnValues() = runTest {
        val dataSource = mock<ComplexDataSource>()
        
        // Setup different return values for different inputs
        everySuspend { dataSource.fetchData("user1") } returns "data1"
        everySuspend { dataSource.fetchData("user2") } returns "data2"
        
        assertEquals("data1", dataSource.fetchData("user1"))
        assertEquals("data2", dataSource.fetchData("user2"))
    }

    // Example: Testing a use case with a mocked dependency
    class FetchDataUseCase(
        private val dataSource: ComplexDataSource
    ) {
        suspend fun execute(id: String): Result<String> {
            return try {
                val data = dataSource.fetchData(id)
                Result.success(data)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }

    @Test
    fun testUseCaseWithMock() = runTest {
        // Given
        val dataSource = mock<ComplexDataSource>()
        everySuspend { dataSource.fetchData("123") } returns "user-data"
        
        val useCase = FetchDataUseCase(dataSource)
        
        // When
        val result = useCase.execute("123")
        
        // Then
        assertTrue(result.isSuccess)
        assertEquals("user-data", result.getOrNull())
        verifySuspend { dataSource.fetchData("123") }
    }

    @Test
    fun testUseCaseErrorHandling() = runTest {
        // Given
        val dataSource = mock<ComplexDataSource>()
        everySuspend { 
            dataSource.fetchData("error") 
        } throws IllegalStateException("Network error")
        
        val useCase = FetchDataUseCase(dataSource)
        
        // When
        val result = useCase.execute("error")
        
        // Then
        assertTrue(result.isFailure)
        assertEquals("Network error", result.exceptionOrNull()?.message)
    }

    // Example: Regular (non-suspend) interface mocking
    interface SimpleCache {
        fun get(key: String): String?
        fun put(key: String, value: String)
        fun clear()
    }

    @Test
    fun testNonSuspendMocking() {
        val cache = mock<SimpleCache>()
        
        // Use every (not everySuspend) for regular functions
        dev.mokkery.every { cache.get("key") } returns "value"
        
        val result = cache.get("key")
        
        assertEquals("value", result)
        verify { cache.get("key") }
    }
}

/**
 * Example: When to use a Manual Fake instead of Mokkery.
 * 
 * For simple interfaces, manual fakes are preferred:
 * - Easier to understand and debug
 * - No magic or code generation
 * - Works without any framework
 * - Better for simple state management
 */
interface FibonacciRepository {
    suspend fun saveFibonacci(value: Int)
    suspend fun getAllFibonacci(): List<Int>
}

// Manual Fake - Preferred for simple interfaces!
class FakeFibonacciRepository : FibonacciRepository {
    val savedValues = mutableListOf<Int>()
    
    override suspend fun saveFibonacci(value: Int) {
        savedValues.add(value)
    }
    
    override suspend fun getAllFibonacci(): List<Int> {
        return savedValues
    }
}

class ManualFakeExampleTest {
    @Test
    fun testWithManualFake() = runTest {
        // No mocking framework needed!
        val repository = FakeFibonacciRepository()
        
        repository.saveFibonacci(1)
        repository.saveFibonacci(1)
        repository.saveFibonacci(2)
        
        val result = repository.getAllFibonacci()
        
        assertEquals(listOf(1, 1, 2), result)
        // Can directly inspect the fake's state
        assertEquals(3, repository.savedValues.size)
    }
}
