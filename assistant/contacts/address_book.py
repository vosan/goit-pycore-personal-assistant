"""
Defines the AddressBook class, which manages multiple contacts.

Responsibilities:
- Store and retrieve Record instances by name.
- Provide search, delete, and iteration methods.
- Include the `get_upcoming_birthdays()` function.
"""

# метод пошуку контактів в клас AddressBook
class AddressBook:
    # треба щоб хтось реалізував
    
    # метод пошуку контактів
    @input_error
    def search_contacts(self, query: str) -> list:
        """Шукає контакти за запитом (ім'я, телефон, email)."""
        results = []
        query_lower = query.lower()
        
        # пошук по всіх полях контакту (структуру треба щоб хтось реалізував)
        for contact in self.data.values():
            if query_lower in contact.name.lower():
                results.append(contact)
                continue
                # пошук в телефонах
            for phone in contact.phones:
                if query in phone: # Телефони зберігаються в рядках, можна шукати без зміни регістру
                    results.append(contact)
                    break
                    # пошук в emails
            for email in contact.emails:
                if query_lower in email.lower():
                    results.append(contact)
                    break
                    
        return results