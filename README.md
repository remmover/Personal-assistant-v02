# Personal Assistant

This project is a personal assistant program that helps users manage contacts, notes, and files. It provides features such as storing contact information, searching contacts, managing notes with tags, searching and sorting notes by tags, and organizing files into categories. Additionally, the assistant has the ability to analyze user input and suggest relevant commands.

## Features

1. **Contact Management**
   - Store contacts with names, addresses, phone numbers, email addresses, and birthdays in a contact book.
   - Display a list of contacts whose birthdays are within a specified number of days from the current date.
   - Validate phone numbers and email addresses during contact creation or editing, and notify the user of any incorrect input.
   - Search contacts within the contact book.
   - Edit and delete contact records.

2. **Note Management**
   - Store notes with text information.
   - Add tags (keywords) to notes to describe their topic or subject.
   - Search notes based on tags.
   - Edit and delete notes.

3. **File Organization**
   - Sort files in a specified folder into categories such as images, documents, videos, etc.

4. **Intelligent Command Suggestions**
   - Analyze user input and provide suggestions for the nearest command based on the input.

5. **Currency Exchange and Weather Forecast**
   - Utilize an API provided by a bank to retrieve currency exchange rates.
   - Fetch weather forecast data for any city using a weather API.

## Installation

1. Clone the project repository from GitHub, GitLab, or Bitbucket.
2. Install the required dependencies using Poetry:
   ```shell
   $ poetry install
   ```
3. Set up the API credentials for the bank and weather services by following the instructions provided in the respective API documentation.
4. Run the program:
   ```shell
   $ poetry run python personal_assistant.py
   ```

## Usage

Once the program is running, you can interact with the personal assistant through the command-line interface. Use the available commands to manage contacts, notes, and files. The assistant will provide suggestions based on your input to assist you in using the correct commands.

Example commands:

- `add contact`: Add a new contact to the contact book.
- `list contacts`: Display the list of contacts.
- `search contacts`: Search for contacts by name or other criteria.
- `add note`: Add a new note with optional tags.
- `search notes`: Search for notes using tags.
- `organize files`: Sort files in a folder into categories.
- `currency exchange`: Get the latest currency exchange rates.
- `weather forecast`: Retrieve the weather forecast for a specific city.

Refer to the program's documentation for more detailed instructions on each command and its usage.

## Data Persistence

The personal assistant stores the information (contacts, notes, and files) on the local hard disk in the user's folder. This ensures that the data is persisted and can be accessed even after restarting the program.

## Conclusion

The personal assistant project provides a versatile tool for managing contacts, notes, and files. It incorporates intelligent command suggestions to enhance the user experience. Additionally, it offers features like currency exchange rates and weather forecasts through the integration of external APIs.

Feel free to explore the project, provide feedback, and suggest improvements!
