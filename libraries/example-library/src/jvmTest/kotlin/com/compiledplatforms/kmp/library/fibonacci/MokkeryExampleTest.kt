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
 * Runs on JVM only; Mokkery does not support JS/Wasm.
 */
class MokkeryExampleTest {

    interface ComplexDataSource {
        suspend fun fetchData(id: String): String
        suspend fun saveData(id: String, data: String)
        suspend fun deleteData(id: String)
        suspend fun listAll(): List<String>
        suspend fun count(): Int
        suspend fun clear()
    }

    @Test
    fun testBasicMocking() = runTest {
        val dataSource = mock<ComplexDataSource>()
        everySuspend { dataSource.fetchData("123") } returns "test-data"
        val result = dataSource.fetchData("123")
        assertEquals("test-data", result)
        verifySuspend { dataSource.fetchData("123") }
    }

    @Test
    fun testMockingWithAnyMatcher() = runTest {
        val dataSource = mock<ComplexDataSource>()
        everySuspend { dataSource.fetchData(any()) } returns "default-data"
        assertEquals("default-data", dataSource.fetchData("123"))
        assertEquals("default-data", dataSource.fetchData("456"))
    }

    @Test
    fun testMockingWithException() = runTest {
        val dataSource = mock<ComplexDataSource>()
        everySuspend {
            dataSource.fetchData("error")
        } throws IllegalStateException("Not found")
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
        dataSource.saveData("1", "data1")
        dataSource.saveData("2", "data2")
        verifySuspend { dataSource.saveData("1", "data1") }
        verifySuspend { dataSource.saveData("2", "data2") }
    }

    @Test
    fun testDifferentReturnValues() = runTest {
        val dataSource = mock<ComplexDataSource>()
        everySuspend { dataSource.fetchData("user1") } returns "data1"
        everySuspend { dataSource.fetchData("user2") } returns "data2"
        assertEquals("data1", dataSource.fetchData("user1"))
        assertEquals("data2", dataSource.fetchData("user2"))
    }

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
        val dataSource = mock<ComplexDataSource>()
        everySuspend { dataSource.fetchData("123") } returns "user-data"
        val useCase = FetchDataUseCase(dataSource)
        val result = useCase.execute("123")
        assertTrue(result.isSuccess)
        assertEquals("user-data", result.getOrNull())
        verifySuspend { dataSource.fetchData("123") }
    }

    @Test
    fun testUseCaseErrorHandling() = runTest {
        val dataSource = mock<ComplexDataSource>()
        everySuspend {
            dataSource.fetchData("error")
        } throws IllegalStateException("Network error")
        val useCase = FetchDataUseCase(dataSource)
        val result = useCase.execute("error")
        assertTrue(result.isFailure)
        assertEquals("Network error", result.exceptionOrNull()?.message)
    }

    interface SimpleCache {
        fun get(key: String): String?
        fun put(key: String, value: String)
        fun clear()
    }

    @Test
    fun testNonSuspendMocking() {
        val cache = mock<SimpleCache>()
        dev.mokkery.every { cache.get("key") } returns "value"
        assertEquals("value", cache.get("key"))
        verify { cache.get("key") }
    }
}

interface FibonacciRepository {
    suspend fun saveFibonacci(value: Int)
    suspend fun getAllFibonacci(): List<Int>
}

class FakeFibonacciRepository : FibonacciRepository {
    val savedValues = mutableListOf<Int>()
    override suspend fun saveFibonacci(value: Int) { savedValues.add(value) }
    override suspend fun getAllFibonacci(): List<Int> = savedValues
}

class ManualFakeExampleTest {
    @Test
    fun testWithManualFake() = runTest {
        val repository = FakeFibonacciRepository()
        repository.saveFibonacci(1)
        repository.saveFibonacci(1)
        repository.saveFibonacci(2)
        assertEquals(listOf(1, 1, 2), repository.getAllFibonacci())
        assertEquals(3, repository.savedValues.size)
    }
}
