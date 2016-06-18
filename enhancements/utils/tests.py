from django.test import SimpleTestCase

from .html import standardize, summarize


class HTMLTestCase(SimpleTestCase):

    INSTALLED_APPS = []

    def test_standardize(self):
        html = '<b>12<script>3</script>'

        self.assertEqual(standardize(html), '<b>12</b>')

    def test_summarize(self):
        html = """
        <p> Line 1 </p>
        <p> Line 2 </p>
        <p> Line 3 </p>
        <p> Line 4 </p>
        <p> Line 5 </p>
        <p> Line 6 </p>
        <p> Line 7 </p>
        <p> Line 8 </p>
        <a href="/"> Link </a>
        <img src="img" />
        <br/>
        <ul>
            <li> List 1 </li>
            <li> List 2 </li>
        </ul>"""

        self.assertEqual(summarize(html), """Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
[ Link ](/) ![](img)  
  * List 1 
  * List 2 
"""
                         )
