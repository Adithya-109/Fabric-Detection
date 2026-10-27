"""Static checks on the web UI: branding, empty initial state, no stale hard-coded statistics."""
import os
import re
import unittest

from tests import ROOT

HTML = open(os.path.join(ROOT, "backend", "templates", "index.html"), encoding="utf-8").read()
JS = open(os.path.join(ROOT, "backend", "static", "js", "app.js"), encoding="utf-8").read()
CSS = open(os.path.join(ROOT, "backend", "static", "css", "style.css"), encoding="utf-8").read()


class TestBranding(unittest.TestCase):
    def test_site_is_called_fabric_classifier(self):
        self.assertIn("<title>Fabric Classifier", HTML)
        self.assertIn('class="brand-name">Fabric Classifier', HTML)

    def test_old_name_is_gone_everywhere(self):
        for label, text in (("html", HTML), ("js", JS), ("css", CSS)):
            self.assertNotRegex(text, r"(?i)texclassifier", label)
        launcher = open(os.path.join(ROOT, "run_web.py"), encoding="utf-8").read()
        self.assertNotRegex(launcher, r"(?i)texclassifier")


class TestNoOvals(unittest.TestCase):
    def test_removed_pill_elements(self):
        for cls in ("sys-badge", "hero-tag", "upload-chips", "hero-stats", "badge-hover-pill"):
            self.assertNotIn(f'class="{cls}', HTML, cls)
            self.assertNotIn(f'"{cls} ', HTML)


class TestEmptyInitialState(unittest.TestCase):
    def test_dashboard_starts_empty(self):
        self.assertRegex(HTML, r'<section class="view-dashboard[^"]*\bdash-empty\b')

    def test_no_prefilled_statistics_in_markup(self):
        for stale in ("66.57", "66.09", "9.10%", "6.86%", "3.58", "2.18", "1000&times;1000", "Hemp",
                      "Natural Flax Fiber", "Crisp slub weave", "EfficientNet", "Apple Silicon"):
            self.assertNotIn(stale, HTML, stale)

    def test_no_preselected_image(self):
        self.assertNotRegex(HTML, r'<img id="preview-img" src="/api')
        self.assertNotIn('qs-pill active', HTML)

    def test_empty_notes_exist_for_result_cards(self):
        self.assertGreaterEqual(HTML.count('class="empty-note"'), 3)  # prediction, contenders, diagnostics (patches has its own placeholder)

    def test_css_hides_results_while_empty(self):
        self.assertRegex(CSS, r"\.dash-empty[^{]*\.pred-body")
        self.assertRegex(CSS, r"\.dash-empty[^{]*\.diag-grid")

    def test_js_does_not_preload_a_sample(self):
        tail = JS[JS.index("18. App Initialization"):]
        self.assertNotIn("selectSample(", tail)

    def test_js_clears_and_restores_empty_state(self):
        self.assertIn("setDashboardEmpty(true)", JS)
        self.assertIn("setDashboardEmpty(false)", JS)

    def test_new_image_starts_classification_automatically(self):
        body = JS[JS.index("function onFileSelected"):JS.index("function setIngestionState")]
        self.assertIn("executeClassification()", body)


class TestPatchCard(unittest.TestCase):
    def test_seven_patch_card_restored_with_honest_caption(self):
        self.assertIn("7-Patch Multi-Crop", HTML)
        self.assertIn("prediction is made from the whole image", HTML)
        self.assertIn("Patch ${idx}", JS)


class TestModelAgnosticCopy(unittest.TestCase):
    def test_pipeline_text_not_tied_to_one_model(self):
        self.assertNotIn("EfficientNet", JS)
        self.assertNotIn("7 garment interior patches", JS)


if __name__ == "__main__":
    unittest.main()
