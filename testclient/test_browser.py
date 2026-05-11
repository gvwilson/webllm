def test_home_page_title(page, server_url):
    page.goto(server_url)
    assert "Sasquatch Sightings" in page.title()


def test_home_page_has_table(page, server_url):
    page.goto(server_url)
    assert page.locator("table").count() == 1


def test_click_sighting_link(page, server_url):
    page.goto(server_url)
    page.locator("table a").first.click()
    page.wait_for_url("**/sighting/**")
    assert "Sighting" in page.title()


def test_add_sighting(page, server_url):
    page.goto(f"{server_url}/add")
    page.fill('[name="species"]', "G. canadensis")
    page.fill('[name="color"]', "brown")
    page.fill('[name="datetime"]', "2024-06-15 09:30")
    page.fill('[name="latitude"]', "49.5")
    page.fill('[name="longitude"]', "-123.1")
    page.click('[type="submit"]')
    page.wait_for_url(server_url + "/")
    assert page.url == server_url + "/"
