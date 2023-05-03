# TeleCourse: Telegram Course Backup Tool

This Python script allows you to backup your courses on Telegram groups. It sorts each folder in the course as a section and creates a thread for each section in the Telegram group. It then uploads videos and related files of every section to their respective threads.

## Features

-   Automatically sorts each folder in the course as a section
-   Creates a thread for each section in the Telegram group
-   Uploads videos and related files of every section to their respective threads
-   Works in reverse manner, meaning uploading of content will start from last section

## How to use

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Create a Telegram group and add the bot to the group
4. Create & Modify the `.env` file according to your needs:
    - `api_id`: The API ID (Get it from [Telegram API Development Tools](https://my.telegram.org/apps))
    - `api_hash` : The API Hash (Get it from [Telegram API Development Tools](https://my.telegram.org/apps))
5. Run the script: `python main.py`

## Contributing

Contributions are welcome! If you find any bugs or want to add a new feature, feel free to open an issue or a pull request.

## Disclaimer

This project was made for educational purposes only. The code may not be the most effective or efficient way to achieve the desired results, and it may contain bugs or errors. Contributions and reports are welcome to help improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
