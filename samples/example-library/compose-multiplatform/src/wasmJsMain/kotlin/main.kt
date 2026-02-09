import androidx.compose.ui.window.ComposeViewport
import com.compiledplatforms.kmp.library.fibonacci.sample.App
import kotlinx.browser.document

fun main() {
    ComposeViewport(document.body!!) {
        App()
    }
}
