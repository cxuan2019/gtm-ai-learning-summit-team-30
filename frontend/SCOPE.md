## 1. Project Overview
This document defines the scope of work for developing the frontend service of the E-Commerce Campaign Landing Page. The application will be built using Next.js, consume external backend APIs for dynamic data, and be deployed as a containerized service to Google Cloud Run.

## 2. In Scope
The following items are officially part of the project deliverables:

*   **Next.js Application Setup:** Initialization of the Next.js (App Router) project with TypeScript, ESLint, and styling configuration (Tailwind CSS or CSS Modules).
*   **UI/UX Development:**
    *   Global Header (Navigation, Utility links) and Footer.
    *   Hero Campaign Carousel.
    *   "Shop by Sport" horizontal slider.
    *   Responsive design ensuring cross-device compatibility (Mobile, Tablet, Desktop).
*   **Backend API Integration:**
    *   Developing services to fetch dynamic product and campaign data from provided backend REST/GraphQL endpoints.
    *   Handling API loading states, error boundaries, and empty states gracefully within the UI.
    *   Implementing Next.js caching strategies (ISR/SSR) to optimize backend load times.
*   **Dockerization:** Creating a multi-stage `Dockerfile` optimized for Next.js standalone builds.
*   **Deployment Configuration:** Setup instructions and configuration for deploying the Docker container to GCP Cloud Run, including environment variable mapping.

## 3. Out of Scope
The following items are explicitly excluded from this project phase:

*   **Backend Service Development:** Building, maintaining, or modifying the backend API infrastructure or database. It is assumed the backend team will provide stable, documented endpoints.
*   **Authentication/Authorization:** Implementing user login, registration, or session management (unless strictly handled via simple pass-through tokens to the API).
*   **Checkout & Payment Processing:** Integration with payment gateways (e.g., Stripe, PayPal). The frontend will direct users to a separate, existing checkout flow or PLP/PDP (Product Listing/Detail Pages).
*   **CI/CD Pipeline Construction:** Writing GitHub Actions, GitLab CI, or Cloud Build YAML files (beyond the base `Dockerfile` required for the container).
*   **Content Creation:** Sourcing raw imagery, writing copywriting, or providing translations for localization.

## 4. Assumptions & Dependencies
*   **API Readiness:** The backend API is fully developed, stable, and comprehensive documentation (e.g., Swagger/OpenAPI) is available prior to the development phase.
*   **Design Assets:** High-fidelity mockups, responsive specifications, and finalized brand assets (fonts, logos, SVGs) are provided.
*   **GCP Access:** The development/DevOps team has the necessary IAM permissions to provision and deploy to Google Cloud Run and Secret Manager.