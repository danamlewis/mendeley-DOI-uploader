# Mendeley DOI Importer

This repository provides a step-by-step guide and Python scripts to add documents to your Mendeley library using their DOIs. The process includes creating an app on Mendeley, getting an access token, extracting DOIs from text using ChatGPT, preparing a text file with the DOI list, and running the script to import the documents to Mendeley.

## 1. Create an app on Mendeley

1. Go to the [Mendeley Developer Portal](https://dev.mendeley.com/).
2. Sign in with your Mendeley credentials.
3. Click on the "My Apps" link in the top-right corner.
4. Click on the "Create App" button.
5. Fill in the required fields:
   - Name: Choose a name for your app.
   - Description: Write a brief description of your app.
   - Redirect URL: Use `https://localhost` for personal use.
6. Click "Create App" to finish the process.

You should see an ID number (e.g. 1234, which is you Client_ID), your app name, and the Client_Secret. You'll  need the Client_ID and Client-Secret.

## 2. Get an access token 

Open your browser. Paste this URL, and put in your client ID (four digit number) where it says 'YOUR_CLIENT_ID':
`https://api.mendeley.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=all`

It will return an error page but look at the browser URL bar again. Mendeley will redirect you to a URL that looks like http://localhost/?code=AUTHORIZATION_CODE. 

Copy the AUTHORIZATION_CODE from the URL.

Then, paste it in to `get-mendeley-token.py` along with your Client_ID and your Client_Secret. Make sure to save the file, then run it (`python get-mendeley-token.py`). Copy the output and save it somewhere as your access token. 

## 3. Extract DOIs from text using ChatGPT

1. Use ChatGPT, ask it to "Make a list of DOIs from this paragraph" (or notes or whatever), followed by pasting in the paragraph. 
2. Copy the extracted DOIs for use in the next step.

## 4. Create a text file with the DOI list

1. Open your terminal and create a new text file, e.g. `vi dois.txt`
2. Paste the extracted DOIs into the file, one per line.
3. Make sure to save the file with a `.txt` extension (e.g., `dois.txt`).

## 5. Use the script to import DOIs to Mendeley

1. Clone this repository or download the Python script `upload-DOI-to-library.py`.
2. Open the script in a text editor and replace `YOUR_ACCESS_TOKEN` with your Mendeley access token generated from step 2. 
3. Update the `dois_file` variable to the path of your text file containing the list of DOIs (if you made it in a different file, also check to make sure it matches the name you gave it).
4. Run the script from the command line: `python upload-DOI-to-library.py`.
5. The script will import each document with the available metadata to your Mendeley library. You can open your library in a browser and watch them get added as it syncs; you can also see a list of all the DOIs it added via the command line.

Example output when the script successfully finishes:

<img width="545" alt="Screen Shot 2023-03-24 at 12 34 12 PM" src="https://user-images.githubusercontent.com/7468165/227631900-470fa129-2910-4923-936f-57066aa8c3d7.png">


## Tips

* You may need to repeat step two to run `get-mendeley-token.py` again and generate an updated access token, and updated it in step 5's script (`upload-DOI-to-library.py`) before running it again if it has been a few hours or more since you last ran the script.
