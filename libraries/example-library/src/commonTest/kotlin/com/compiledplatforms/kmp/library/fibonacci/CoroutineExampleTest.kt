package com.compiledplatforms.kmp.library.fibonacci

import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

/**
 * Example tests demonstrating kotlinx-coroutines-test usage.
 * 
 * These tests show how to:
 * - Test suspend functions with runTest
 * - Test delays and timing with virtual time
 * - Test coroutine-based code
 */
class CoroutineExampleTest {

    @Test
    fun testSuspendFunction() = runTest {
        // runTest provides a test coroutine scope with virtual time
        val result = fetchFibonacciAsync(5)
        assertEquals(5, result)
    }

    @Test
    fun testDelayWithVirtualTime() = runTest {
        // Delays are skipped in virtual time - this test runs instantly
        val result = delayedFibonacci()
        
        // The delay happened instantly in virtual time
        assertEquals(2, result)
    }

    @Test
    fun testMultipleSuspendCalls() = runTest {
        val results = mutableListOf<Int>()
        
        repeat(3) {
            results.add(fetchFibonacciAsync(it))
        }
        
        assertEquals(listOf(0, 1, 2), results)
    }

    // Example suspend functions to test
    private suspend fun fetchFibonacciAsync(n: Int): Int {
        delay(10) // Simulated async work
        return when (n) {
            0 -> 0
            1 -> 1
            else -> n
        }
    }

    private suspend fun delayedFibonacci(): Int {
        delay(1000) // This delay is skipped in virtual time
        return 2
    }

    // Example Flow for testing
    private fun fibonacciFlow(): Flow<Int> = flow {
        emit(0)
        delay(100)
        emit(1)
        delay(100)
        emit(1)
        delay(100)
        emit(2)
    }
}
