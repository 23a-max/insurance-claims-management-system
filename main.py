
from database import create_tables
from claims import register_claim, view_claims , update_claim_status


def main():
    create_tables()

    while True:
        print("\n===================================")
        print(" INSURANCE CLAIMS MANAGEMENT SYSTEM")
        print("===================================")
        print("1. Register a new claim")
        print("2. View all claims")
        print("3. Update claim status")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_claim()
        elif choice == "2":
            view_claims()
        elif choice == "3":
            update_claim_status()
        elif choice == "4":
            print("Thank you have a nice day")
            break    
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
