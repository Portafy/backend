
# Project To-Do List

This document outlines the remaining tasks to complete the PDF-to-Website project, based on the features described in the `README.md`.

---

## Backend (Django)

-   [ ] **Manual Content Entry API:**
    -   [ ] Create a new endpoint (e.g., `/api/websites/manual/`) to accept structured JSON data for website content (experience, education, etc.).
    -   [ ] Add a `content_type` field to the `Website` model to distinguish between `pdf` and `manual` entries.
    -   [ ] Write a serializer to validate and process the manually entered data.

-   [ ] **Content Editor API:**
    -   [ ] Implement a `PUT` or `PATCH` endpoint (e.g., `/api/websites/<slug>/content/`) to allow users to update the parsed or manually entered website content.
    -   [ ] Ensure this endpoint is secure and only accessible by the website owner.

-   [ ] **Payment Integration:**
    -   [ ] Integrate a payment provider like Stripe or PayPal into the `payments` app.
    -   [ ] Create an endpoint to initiate a payment session.
    -   [ ] Implement a webhook to listen for successful payment events and update the user's account status.

-   [ ] **Source Code Download:**
    -   [ ] Create a function that generates a ZIP archive of the website's static files (`index.html`, `style.css`, assets).
    -   [ ] Develop a secure endpoint (e.g., `/api/websites/<slug>/download/`) that allows a user with a successful payment to download this ZIP file.

-   [ ] **Theme Management:**
    -   [ ] Finalize the `ThemeConfig` model to store theme-specific settings (colors, fonts, layout).
    -   [ ] Create an API endpoint to list available themes for the frontend.

-   [ ] **Testing:**
    -   [ ] Write unit and integration tests for all new API endpoints.
    -   [ ] Ensure existing tests are updated to reflect new model changes.

---

## Frontend (React)

-   [ ] **Project Setup:**
    -   [ ] Set up routing with a library like `react-router-dom`.
    -   [ ] Configure a state management solution (e.g., Redux Toolkit, Zustand, or Context API).
    -   [ ] Set up an API client (e.g., Axios) to communicate with the Django backend.

-   [ ] **User Authentication:**
    -   [ ] Build Login, Register, and Logout components.
    -   [ ] Create protected routes that are only accessible to authenticated users.

-   [ ] **Core UI Components:**
    -   [ ] **Dashboard/Home Page:** A central page where users can see their existing websites or start creating a new one.
    -   [ ] **Creation Method Choice:** A UI component that lets the user choose between "Upload PDF" and "Enter Manually".

-   [ ] **Website Creation Flow:**
    -   [ ] **PDF Upload Component:** A form for uploading the PDF file.
    -   [ ] **Manual Entry Form:** A multi-step form for users to enter their information section by section.
    -   [ ] **Editor & Live Preview:**
        -   [ ] An editor view with form fields populated by the parsed PDF or manual entry.
        -   [ ] A live preview pane that renders the website and updates in real-time as the user edits the content.
    -   [ ] **Theme Selector:** A component to display available themes and apply them to the live preview.

-   [ ] **Publishing and Payment:**
    -   [ ] A "Publish" button that finalizes the website content.
    -   [ ] A dedicated page or modal for handling the payment flow.
    -   [ ] A success page with the link to the published site and a button to download the source code (if paid).

-   [ ] **Styling:**
    -   [ ] Ensure the entire application is responsive and mobile-friendly.
    -   [ ] Implement a consistent and clean design, possibly using a UI library like Material-UI or Chakra UI.

---

## DevOps & Deployment

-   [ ] **Production Environment:**
    -   [ ] Set up a production-ready database (e.g., PostgreSQL).
    -   [ ] Configure a production web server (e.g., Gunicorn + Nginx).
    -   [ ] Set up hosting for the Django backend (e.g., Heroku, DigitalOcean, Vercel).
    -   [ ] Set up hosting for the React frontend (e.g., Netlify, Vercel).

-   [ ] **CI/CD Pipeline:**
    -   [ ] Enhance the existing `ci.yml` to automatically run tests on every push.
    -   [ ] Add a deployment step to automatically deploy the backend and frontend to production on merges to the `main` branch.

-   [ ] **Object Storage:**
    -   [ ] Configure Amazon S3 or a similar service to store user-uploaded PDFs and other media files instead of the local filesystem.
