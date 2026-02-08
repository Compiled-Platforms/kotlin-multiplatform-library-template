package com.compiledplatforms.kmp.library.fibonacci.sample

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.compiledplatforms.kmp.library.fibonacci.generateFibi

@Composable
fun App() {
    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                Text(
                    text = "Example Library – Fibonacci Sample",
                    style = MaterialTheme.typography.headlineMedium,
                    modifier = Modifier.padding(bottom = 24.dp)
                )

                FibonacciSequenceCard()
            }
        }
    }
}

@Composable
fun FibonacciSequenceCard() {
    val first10 = generateFibi().take(10).toList()
    val sum = generateFibi().take(10).sum()
    val under100 = generateFibi().takeWhile { it < 100 }.toList()

    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "First 10 Fibonacci numbers",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(bottom = 12.dp)
            )
            Text(
                text = first10.joinToString(", "),
                style = MaterialTheme.typography.bodyMedium
            )

            Text(
                text = "Sum of first 10",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(top = 16.dp, bottom = 12.dp)
            )
            Text(
                text = sum.toString(),
                style = MaterialTheme.typography.bodyMedium
            )

            Text(
                text = "Values less than 100",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(top = 16.dp, bottom = 12.dp)
            )
            Text(
                text = under100.joinToString(", "),
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}
