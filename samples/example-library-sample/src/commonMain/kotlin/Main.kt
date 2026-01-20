package io.github.kotlin.fibonacci

/**
 * Sample application demonstrating the use of example-library.
 * 
 * This sample shows how to:
 * - Import and use the Fibonacci sequence generator
 * - Take a limited number of elements from the sequence
 * - Print the results
 */
fun main() {
    println("=== Example Library Sample ===")
    println()
    
    // Generate the first 10 Fibonacci numbers
    println("First 10 Fibonacci numbers:")
    val fibSequence = generateFibi().take(10).toList()
    fibSequence.forEachIndexed { index, value ->
        println("F($index) = $value")
    }
    
    println()
    
    // Calculate the sum of first 10 Fibonacci numbers
    val sum = generateFibi().take(10).sum()
    println("Sum of first 10 Fibonacci numbers: $sum")
    
    println()
    
    // Find Fibonacci numbers less than 100
    println("Fibonacci numbers less than 100:")
    val fibUnder100 = generateFibi().takeWhile { it < 100 }.toList()
    println(fibUnder100.joinToString(", "))
}
