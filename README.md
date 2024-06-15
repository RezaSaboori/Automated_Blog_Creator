# Automated_Blog_Creator

This project parses RSS feeds, analyzes the content using a Large Language Model (LLM), selects relevant articles, and automatically creates a blog from the selected content.

## Features

- Parse RSS feeds
- Check proxy speeds and manage proxies
- Extract main content from web pages
- Store content in MongoDB
- Analyze content with LLM
- Automatically create blog posts

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/reza74rsa/Automated_Blog_Creator.git
    cd Automated_Blog_Creator
    ```
2. Create the Virtual Environment:
    ```sh
    python3 -m venv venv
    cd venv/bin
    source activate
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Modify the configuration settings in `src/config.py` (if applicable).

2. Run the Jupyter Notebook:
    ```sh
    jupyter notebook main.ipynb
    ```

3. Follow the instructions in the notebook to parse RSS feeds, check proxies, extract content, and analyze it.

## Project Structure

- `main.ipynb`: Main Jupyter Notebook to run the project.
- `src/`: Directory containing source code files.
  - `feed_parser.py`: Functions for parsing RSS feeds.
  - `proxy_checker.py`: Functions for checking and managing proxies.
  - `content_extractor.py`: Functions for extracting main content from web pages.
- `requirements.txt`: List of dependencies.
- `.gitignore`: Git ignore file.

## License

This project is licensed under the MIT License.
