# ☕️ Coffee Agent

**LLM-powered multi-agent coffee shop assistant** built with FastAPI backend, Streamlit frontend, and local LLM (via Ollama). This system supports user interaction, coffee ordering, menu exploration, and smart recommendations — all through conversational chat.

---


## 🚀 Features

- 🔐 **User Authentication**  
  Register and log in securely via FastAPI APIs.

- 💬 **Conversational Chat Interface**  
  Interact with the assistant through a friendly Streamlit-based UI.

- 🧠 **Multi-Agent Architecture**  
  Modular agents handle classification, recommendations, order processing, and more — making the system highly maintainable and scalable.

- 🛒 **Direct Ordering via Chat**  
  Users can browse, customize, and order coffee products naturally through conversation.

- 💾 **Persistent Chat History**  
  All user interactions are stored in a PostgreSQL database for tracking and personalization.

- 🖥️ **Offline-First with Ollama**  
  Runs completely offline with local LLM models using [Ollama](https://ollama.com).

- 🐳 **Fully Dockerized Setup**  
  FastAPI, Streamlit, and PostgreSQL run in isolated containers with a unified Docker Compose setup.

- 🔍 **Product Search & Details Retrieval**  
  Ask for information about coffee items (e.g., origin, ingredients, taste notes) using intelligent semantic search powered by FAISS vector stores.

- 🎯 **Intent Classification**  
  Incoming user inputs are automatically routed to the correct agent using `classification_agent.py`.

- 📈 **Smart Recommendations**  
  Suggests items based on:
  - Apriori association rules (`apriori_recommendation.json`)
  - Popularity-based data (`popularity_recommendation.csv`)

- 🛡️ **Input Moderation & Validation**  
  All user queries are filtered and validated using `guard_agent.py` to ensure a safe, appropriate chat environment.

- 📦 **Embedded Knowledge Base**  
  Uses FAISS indices (`faiss_product.index`, `bge_vector_store.index`) for fast, contextual product retrieval.

- 🔄 **Modular & Extendable Agent Protocols**  
  Easily add or modify agents via shared protocols defined in `agent_protocol.py`.

- 🧪 **Development Utilities**  
  Contains helper scripts in `development_code.py` for testing, extending, or debugging the application.

---

## 🧑‍💼 Agents Overview

The app is powered by **five intelligent agents**, each handling a specific task:

- `classification_agent.py` – Determines the user's intent (order, ask for details, etc.).
- `details_agent.py` – Provides detailed product information like ingredients or origin.
- `guard_agent.py` – Validates requests and filters inappropriate inputs.
- `order_taking_agent.py` – Handles item selection, customization, and order placement.
- `recommendation_agent.py` – Suggests items based on popularity or prior data (Apriori & popularity models).

---

## 📦 Dockerized Architecture

The app runs three containers within a shared network:

- `FastAPI` – Handles API and backend logic.
- `Streamlit` – Offers a chat UI interface for users.
- `PostgreSQL` – Stores user and chat data persistently.

---

## ⚙️ Requirements

- [Ollama](https://ollama.com) – For running local LLM models (e.g., llama3).
- [Docker](https://www.docker.com/) – For running FastAPI, Streamlit, and PostgreSQL in containers.

---

## 🛠️ Installation

```bash
# Step 1: Set up Ollama locally (https://ollama.com/)
# Step 2: Clone the repository
git clone https://github.com/nishantssoni/coffee_agent.git

# Step 3: Navigate into the project directory
cd coffee_agent

# Step 4: Run the containers
docker-compose up
```

---

## 📁 File Structure

├── app
│   ├── agents                  # Modular LLM agents
│   │   ├── classification_agent.py
│   │   ├── details_agent.py
│   │   ├── guard_agent.py
│   │   ├── order_taking_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── agent_protocol.py   # Base protocols/interfaces for agents
│   │   └── utils.py            # Helper functions
│   ├── config.py               # Environment/config variables
│   ├── database.py             # PostgreSQL integration
│   ├── development_code.py     # Dev utilities/scripts
│   ├── index_and_data          # FAISS & embedding stores
│   │   ├── bge_vector_store.index
│   │   ├── data.pkl
│   │   └── faiss_product.index
│   ├── models.py               # Pydantic/SQLAlchemy models
│   ├── oauth2.py               # Auth and token handling
│   ├── recommendation_objects  # Pre-built recommendation datasets
│   │   ├── apriori_recommendation.json
│   │   └── popularity_recommendation.csv
│   ├── routers                 # API routes
│   │   ├── auth.py
│   │   ├── chats.py
│   │   └── users.py
│   ├── schemas.py              # Pydantic schemas
│   └── utils.py                # General-purpose utilities
├── streamlit
│   ├── main.py                 # Streamlit chat UI app
│   ├── Dockerfile              # Streamlit container setup
│   └── requirements.txt
├── docker-compose.yml          # Defines multi-container setup
├── Dockerfile                  # FastAPI container setup
├── .env.example                # Sample environment file


---

## 📸 Screenshots
![Screenshot](ui_demo.png)
![Screenshot](working_demo.png)
---

## 🤝 Contribution
Contributions are welcome! Feel free to open issues or submit pull requests for suggestions, improvements, or bug fixes.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## 📬 Contact
For any questions or feedback, please contact [iamnishantsoni4@gmail.com](mailto:iamnishantsoni4@gmail.com).

---

Let me know if you'd like help designing badges, screenshots, or adding GitHub Actions CI/CD setup.

