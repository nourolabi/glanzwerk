# Streamlit Cloud Deployment Guide for Glanzwerk Invoice System

This guide provides step-by-step instructions on how to deploy the Glanzwerk Invoice System to Streamlit Cloud, making it publicly accessible without any local installation.

## Prerequisites

1.  **GitHub Repository:** Ensure your project is pushed to a GitHub repository. This is essential as Streamlit Cloud directly integrates with GitHub.
2.  **Streamlit Account:** You need a Streamlit Cloud account. If you don't have one, you can sign up at [share.streamlit.io](https://share.streamlit.io/).

## Deployment Steps

1.  **Log in to Streamlit Cloud:**
    *   Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.

2.  **Deploy a new app:**
    *   On your Streamlit Cloud dashboard, click on the "New app" button (usually located on the top right).

3.  **Connect to your GitHub repository:**
    *   In the deployment dialog, select "From existing repo".
    *   Choose the GitHub repository where you pushed the Glanzwerk Invoice System code (e.g., `your-username/glanzwerk-invoice-system`).
    *   Select the branch you want to deploy from (e.g., `main`).
    *   **Main file path:** Enter `app.py` (this is the main Streamlit application file).
    *   **Python version:** Select a compatible Python version (e.g., `3.9` or `3.10`).

4.  **Advanced settings (Optional but Recommended for this project):**
    *   Click on "Advanced settings" to expand the options.
    *   **Secrets:** If your application were to use any API keys or sensitive information, you would add them here. For this project, no specific secrets are required.
    *   **Custom fonts for PDF generation:**
        *   The PDF generation uses `DejaVuSans` font to support German special characters (Umlaute). Streamlit Cloud environments might not have this font pre-installed.
        *   **Solution:** You need to ensure the `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` files are present in your repository, ideally in the same directory as `pdf_generator_new.py` or in a dedicated `fonts` directory.
        *   In `pdf_generator_new.py`, the font paths are currently set to `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` and `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`. **You will need to update these paths** to reflect their location within your GitHub repository. For example, if you place them in a `fonts` folder next to `pdf_generator_new.py`, the paths should be `os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')`.

5.  **Deploy the app:**
    *   Click on the "Deploy!" button.
    *   Streamlit Cloud will now build and deploy your application. This process might take a few minutes.

6.  **Access your deployed app:**
    *   Once the deployment is successful, you will be provided with a public URL to access your Glanzwerk Invoice System.

## Important Notes

*   **Database:** The current implementation uses a SQLite database (`glanzwerk.db`). In a Streamlit Cloud environment, this database will be ephemeral, meaning data will be lost when the app restarts (e.g., due to updates or inactivity). For persistent data storage, you would need to integrate with an external database service (e.g., PostgreSQL, Google Cloud SQL, etc.). For the current scope, the in-memory SQLite is sufficient for demonstration and basic use.
*   **Requirements:** The `requirements.txt` file in your repository lists all necessary Python packages. Streamlit Cloud automatically installs these during deployment.

By following these steps, your Glanzwerk Invoice System will be live and accessible to anyone with the link!

