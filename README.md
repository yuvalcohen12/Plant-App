# Plant-App
# PlantAI - Frontend Web Client

A cross-platform web application built with Flutter that allows users to identify plants via image upload, search for specific care instructions, and manage a personal digital garden. 

## Core Features
* AI Plant Identification: Users can upload images to instantly identify plants and receive tailored care instructions.
* Local Persistence: Utilizes SQLite (sqflite_common_ffi_web) for robust, in-browser local storage, allowing users to save their garden state across sessions.
* Cross-Origin Communication: Fully configured to handle CORS and interact with an external cloud-hosted Python backend.
* Responsive UI: Built with Flutter's widget tree to support both mobile and desktop browser dimensions.

## Tech Stack
* Framework: Flutter / Dart
* Storage: SQLite (Web implementation)
* Networking: HTTP package for REST API communication
* Deployment: GitHub Pages (Static Web Build)
