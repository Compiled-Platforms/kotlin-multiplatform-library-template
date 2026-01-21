package com.compiledplatforms.kmp.library.fibonacci

import io.kotest.matchers.collections.shouldBeEmpty
import io.kotest.matchers.collections.shouldContain
import io.kotest.matchers.collections.shouldHaveSize
import io.kotest.matchers.collections.shouldNotBeEmpty
import io.kotest.matchers.ints.shouldBeGreaterThan
import io.kotest.matchers.ints.shouldBeLessThan
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import io.kotest.matchers.string.shouldContain
import io.kotest.matchers.string.shouldStartWith
import io.kotest.matchers.types.shouldBeInstanceOf
import kotlin.test.Test

/**
 * Example tests demonstrating Kotest assertions for more expressive testing.
 * 
 * This uses only `kotest-assertions-core`, not the full Kotest framework.
 * Tests still use kotlin.test's @Test annotation and structure.
 * 
 * Benefits:
 * - More readable: `result shouldBe 5` vs `assertEquals(5, result)`
 * - Better error messages with actual vs expected clearly shown
 * - Infix syntax reads like natural language
 * - Rich matchers for common scenarios
 */
class KotestAssertionsExampleTest {

    // Compare with kotlin.test style
    @Test
    fun kotlinTestStyle() {
        val sequence = generateFibi().take(5).toList()
        kotlin.test.assertEquals(5, sequence.size)
        kotlin.test.assertTrue(sequence.isNotEmpty())
    }

    @Test
    fun kotestStyle() {
        val sequence = generateFibi().take(5).toList()
        sequence shouldHaveSize 5
        sequence.shouldNotBeEmpty()
    }

    // Numeric assertions
    @Test
    fun testNumericAssertions() {
        val numbers = generateFibi().take(10).toList()
        
        // The first element should be a non-negative integer
        numbers[0] shouldBeGreaterThan -1
        // After 10 iterations, the value should be positive
        numbers[9] shouldBeGreaterThan 0
        // The 6th element should not be zero
        numbers[5] shouldNotBe 0
    }

    // String assertions
    @Test
    fun testStringAssertions() {
        val message = "Fibonacci sequence"
        
        message shouldContain "Fibonacci"
        message shouldStartWith "Fib"
        message shouldNotBe ""
    }

    // Collection assertions
    @Test
    fun testCollectionAssertions() {
        val sequence = generateFibi().take(8).toList()
        
        sequence shouldHaveSize 8
        sequence.shouldNotBeEmpty()
        
        val empty = emptyList<Int>()
        empty.shouldBeEmpty()
    }

    // Type assertions
    @Test
    fun testTypeAssertions() {
        val value: Any = generateFibi().first()
        
        value.shouldBeInstanceOf<Int>()
    }

    // Practical example: Testing Fibonacci sequence
    @Test
    fun testFibonacciSequenceWithKotest() {
        val numbers = generateFibi().take(10).toList()
        
        numbers shouldHaveSize 10
        numbers.shouldNotBeEmpty()
        
        // Verify it's generally increasing (after first few)
        numbers.last() shouldBeGreaterThan numbers.first()
    }

    // Chaining assertions
    @Test
    fun testChainingAssertions() {
        val result = generateFibi().first()
        
        result
            .shouldBeInstanceOf<Int>()
            .let { it shouldBeGreaterThan -1 }
    }

    // Demonstrating better error messages
    @Test
    fun testBetterErrorMessages() {
        val actual = generateFibi().take(5).toList()
        
        // If this fails, Kotest shows:
        // expected:<...> but was:<[actual values]>
        // with clear diff
        actual shouldHaveSize 5
        actual.shouldNotBeEmpty()
    }

    // Negative assertions
    @Test
    fun testNegativeAssertions() {
        val numbers = generateFibi().take(3).toList()
        
        numbers shouldNotBe emptyList<Int>()
        numbers shouldHaveSize 3
    }

    // Multiple assertions in one test
    @Test
    fun testMultipleAssertions() {
        val numbers = generateFibi().take(10).toList()
        
        // All these assertions are clear and readable
        numbers shouldHaveSize 10
        numbers.shouldNotBeEmpty()
        numbers.first().shouldBeInstanceOf<Int>()
        numbers.last() shouldBeGreaterThan numbers.first()
    }
}

/**
 * Comparison: kotlin.test vs Kotest Assertions
 * 
 * kotlin.test:
 * ```kotlin
 * assertEquals(5, result)
 * assertTrue(result > 0)
 * assertNotNull(value)
 * assertTrue(list.contains(5))
 * ```
 * 
 * Kotest:
 * ```kotlin
 * result shouldBe 5
 * result shouldBeGreaterThan 0
 * value shouldNotBe null
 * list shouldContain 5
 * ```
 * 
 * Both work great! Kotest reads more naturally and provides
 * better error messages. kotlin.test is more standard and familiar.
 * 
 * Use whichever style you prefer - they can even be mixed in the same test!
 */
