# Regression Checklist

## 1. Financial Snapshots & Projections (HIGHEST RISK)
**Why:** Deep logic refactor impacting how Best and Worst case snapshots calculate runway and handle previous debt.
**Steps:**
1. Navigate to the Financial Snapshots or Projections page (if available).
2. Look at the Cash Balance and Cash Runway for "Base", "Best", and "Worst" projections.
3. Compare the current month's Cash Balance against the previous month's Cash Balance plus this month's net cash flow.
**Expected Result:** The cash balances for all three cases should correctly carry forward any positive or negative debt from the previous month. The Best case should show lower expenses than the Base case.

## 2. Dashboard Financial Metrics (HIGH RISK)
**Why:** The dashboard now fetches metrics from the latest `Base` snapshot instead of raw `SUM()`s. If snapshots are stale, the dashboard will be stale.
**Steps:**
1. Navigate to the main Dashboard.
2. Note the current Monthly Revenue, Burn Rate, and Cash Balance.
3. Navigate to Operations and add a new "One Time" Revenue entry for this month.
4. Add a new "Critical" Expense entry for this month.
5. Return to the Dashboard and verify the numbers.
**Expected Result:** The Dashboard metrics should reflect the newly added revenue and expenses (assuming the backend triggers a snapshot refresh when new entries are added).

## 3. Client Creation
**Why:** Previously crashed due to a missing default value for `reliability_score`.
**Steps:**
1. Navigate to the Operations page.
2. Fill out the "Add Client" form with a new name and email.
3. Click "Add Client".
**Expected Result:** The client should be created successfully without an error.

## 4. Revenue Creation via Email
**Why:** Changed the revenue creation flow to lookup clients by email instead of name to avoid conflicts.
**Steps:**
1. Navigate to the Operations page.
2. Under Revenue, fill out the form using the email address of the client you just created (instead of their name).
3. Fill out the remaining fields (amount, dates) and submit.
**Expected Result:** The revenue should be successfully added and attributed to the correct client.

## 5. Negative Cash Balance Carry-Forward
**Why:** Previously, negative balances were reset to 0 at the start of a new month.
**Steps:**
1. Navigate to Operations.
2. Add a massive Expense (e.g., $100,000,000) to purposefully push the cash balance deeply negative.
3. Ensure the current month is updated, then add a small Revenue entry (e.g., $10) for the *next* month (you may need to wait for a month boundary or simulate it).
4. View the dashboard/snapshots for that next month.
**Expected Result:** The cash balance should remain massively negative (approx -$100M) rather than resetting to a small positive $10 balance.
