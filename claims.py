
from database import get_connection


def register_claim():
    """Register a new insurance claim."""
    print("\n--- Register New Claim ---")

    customer_name = input("Customer name: ").strip()
    policy_number = input("Policy number: ").strip()
    description = input("Claim description: ").strip()

    try:
        claim_amount = float(input("Claim amount (₹): "))
        if claim_amount <= 0:
            print("Error: Claim amount must be greater than zero.")
            return
    except ValueError:
        print("Error: Please enter a valid numeric amount.")
        return

    if not customer_name or not policy_number or not description:
        print("Error: All fields are required.")
        return

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO claims
                (customer_name, policy_number, claim_amount, description)
            VALUES (?, ?, ?, ?)
            """,
            (customer_name, policy_number, claim_amount, description),
        )
        claim_id = cursor.lastrowid

    print(f"\nClaim registered successfully! Claim ID: {claim_id}")


def view_claims():
    """Display all registered claims."""
    with get_connection() as connection:
        claims = connection.execute(
            "SELECT * FROM claims ORDER BY claim_id DESC"
        ).fetchall()

    if not claims:
        print("\nNo claims found.")
        return

    print("\n--- Insurance Claims ---")
    for claim in claims:
        print("-" * 40)
        print(f"Claim ID:      {claim['claim_id']}")
        print(f"Customer:      {claim['customer_name']}")
        print(f"Policy:        {claim['policy_number']}")
        print(f"Amount:        ₹{claim['claim_amount']:.2f}")
        print(f"Description:   {claim['description']}")
        print(f"Status:        {claim['status']}")

def update_claim_status():
    """Update the status of an existing claim."""
    print("\n--- Update Claim Status ---")

    try:
        claim_id = int(input("Enter claim ID: "))
    except ValueError:
        print("Error: Claim ID must be a number.")
        return

    valid_statuses = [
        "Submitted",
        "Under Review",
        "Approved",
        "Rejected",
    ]

    print("\nAvailable statuses:")
    for status in valid_statuses:
        print(f"- {status}")

    new_status = input("Enter new status: ").strip().title()

    if new_status not in valid_statuses:
        print("Error: Invalid status.")
        return

    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE claims SET status = ? WHERE claim_id = ?",
            (new_status, claim_id),
        )

        if cursor.rowcount == 0:
            print("Error: Claim ID not found.")
        else:
            print("Claim status updated successfully!")
