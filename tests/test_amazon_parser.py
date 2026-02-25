from scraper.parsers.amazon_parser import AmazonParser


def test_parse_valid_product():
    html = """
    <html>
      <body>
        <div class="product">
          <h1 class="product-title">Gaming Mouse X200</h1>
          <span class="price">€49.99</span>
          <div class="availability">In stock</div>
        </div>
      </body>
    </html>
    """

    parser = AmazonParser()
    product = parser.parse(html, "https://fake-url.com")

    assert product.title == "Gaming Mouse X200"
    assert product.price == 49.99
    assert product.currency == "€"
    assert product.availability == "In stock"