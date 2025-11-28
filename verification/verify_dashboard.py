from playwright.sync_api import sync_playwright

def verify_dashboard_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the dashboard page
        try:
            page.goto("http://localhost:4321/", timeout=60000)

            # Check for main headings
            page.wait_for_selector("text=Performance Overview")
            page.wait_for_selector("text=Weekly Performance")
            page.wait_for_selector("text=Active Campaigns")
            page.wait_for_selector("text=Intelligent Insights")

            # Check for Chart presence (recharts usually creates an svg or div structure)
            page.wait_for_selector(".recharts-responsive-container")

            # Check for Table presence
            page.wait_for_selector("table")

            # Check for specific campaign data
            page.wait_for_selector("text=Summer Sale 2024")
            page.wait_for_selector("text=Meta")

            # Take a screenshot
            page.screenshot(path="/home/jules/verification/dashboard_page.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard_page()
