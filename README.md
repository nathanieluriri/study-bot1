title: Botly
emoji: 👀
colorFrom: green
colorTo: purple
sdk: streamlit
sdk_version: 1.44.0
app_file: app.py
pinned: false

## Introduction

StudyBot is a powerful tool designed to enhance your study experience by providing personalized assistance and resources tailored to your learning needs. With StudyBot, you can streamline your study sessions, access relevant materials, and track your progress effortlessly.

## Prerequisites

Before using StudyBot, ensure you have the following prerequisites set up:

1. **OpenAI API Key**: Obtain your OpenAI API key and store it in a `.env` file. The format of the `.env` file should be as follows:

   ```plaintext
   OPENAI_API_KEY="YOUR_API_KEY_HERE"
   ```

2. **MongoDB URI**: If using a local MongoDB database, set the `MONGO_URI` variable in the `.env` file as follows:

   ```plaintext
   MONGO_URI="mongodb://localhost:27017/studybotdb"
   ```

   If using a remote MongoDB database, use a similar format for the `MONGO_URI` variable.

## Installation

Follow these steps to install and set up StudyBot on your system:

1. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:

   ```bash
   venv/Scripts/activate   # For Windows
   ```

   ```bash
   source venv/bin/activate   # For Linux/macOS
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Once you have installed StudyBot and set up the prerequisites, you can run the application using the following command:

```bash
streamlit run app.py
```

This command will start the StudyBot application, and you can access it through your web browser at the provided URL.

## Features

StudyBot offers a range of features to support your study sessions, including:

- **Personalized Assistance**: StudyBot provides personalized recommendations and resources based on your learning preferences and progress.
  
- **Content Generation**: Utilizing the power of OpenAI's GPT-3, StudyBot can generate summaries, explanations, and additional study materials on demand.

- **Interactive Interface**: StudyBot's user-friendly interface makes it easy to navigate and access relevant study materials.

