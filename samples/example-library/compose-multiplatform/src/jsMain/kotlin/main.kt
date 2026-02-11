import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.window.ComposeViewport
import com.compiledplatforms.kmp.library.fibonacci.sample.App
import kotlinx.browser.document

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    val container = requireNotNull(document.body) {
        "document.body is null - ensure script runs after DOM is ready"
    }
    ComposeViewport(container) {
        App()
    }
}
