from tests.base import BootstrapTestCase


class BootstrapLabelTestCase(BootstrapTestCase):
    def test_bootstrap_label(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_label "Subject" %}'),
            '<label class="form-label">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_for='subject' %}"),
            '<label for="subject" class="form-label">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_class='label-class' %}"),
            '<label class="label-class">Subject</label>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_label \"Subject\" label_title='label-title' %}"),
            '<label title="label-title" class="form-label">Subject</label>',
        )
