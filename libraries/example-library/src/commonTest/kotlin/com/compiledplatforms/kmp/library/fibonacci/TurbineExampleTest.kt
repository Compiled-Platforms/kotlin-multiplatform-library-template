package com.compiledplatforms.kmp.library.fibonacci

import app.cash.turbine.test
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

/**
 * Example tests demonstrating Turbine usage for Flow testing.
 * 
 * Turbine makes Flow testing incredibly simple and readable.
 * It provides a fluent API for testing Flow emissions.
 */
class TurbineExampleTest {

    @Test
    fun testFlowEmissions() = runTest {
        fibonacciFlow().test {
            // Test each emission in order
            assertEquals(0, awaitItem())
            assertEquals(1, awaitItem())
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            awaitComplete()
        }
    }

    @Test
    fun testFlowWithSkip() = runTest {
        fibonacciFlow().test {
            // Skip first two emissions
            skipItems(2)
            
            // Test remaining emissions
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            awaitComplete()
        }
    }

    @Test
    fun testFlowError() = runTest {
        errorFlow().test {
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            
            // Test that flow completes with error
            val error = awaitError()
            assertEquals("Fibonacci error", error.message)
        }
    }

    @Test
    fun testFlowCancellation() = runTest {
        infiniteFibonacciFlow().test {
            // Take first 3 items then cancel
            assertEquals(0, awaitItem())
            assertEquals(1, awaitItem())
            assertEquals(1, awaitItem())
            
            cancel() // Cancel the flow
        }
    }

    @Test
    fun testFlowTiming() = runTest {
        fibonacciFlow().test {
            // Turbine works with virtual time from runTest
            val item1 = awaitItem()
            assertEquals(0, item1)
            
            // No need to manually advance time - it's automatic
            val item2 = awaitItem()
            assertEquals(1, item2)
            
            skipItems(2)
            awaitComplete()
        }
    }

    // Example Flows for testing
    private fun fibonacciFlow(): Flow<Int> = flow {
        emit(0)
        delay(100)
        emit(1)
        delay(100)
        emit(1)
        delay(100)
        emit(2)
    }

    private fun errorFlow(): Flow<Int> = flow {
        emit(1)
        emit(2)
        throw IllegalStateException("Fibonacci error")
    }

    private fun infiniteFibonacciFlow(): Flow<Int> = flow {
        var a = 0
        var b = 1
        
        while (true) {
            emit(a)
            delay(100)
            val next = a + b
            a = b
            b = next
        }
    }
}
