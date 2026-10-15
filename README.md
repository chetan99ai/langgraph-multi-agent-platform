# 🚀 LangGraph Multi-Agent Platform (Serverless AWS Bedrock AgentCore & Local Studio Blueprint)

This repository contains a production-grade, generic, and highly scalable multi-agent platform orchestrating containerized **LangGraph** workflows. 

It is natively designed to support local testing using **LangGraph Studio**, handles enterprise-grade automation via **GitHub Actions CI/CD pipelines**, and provisions serverless **Amazon Bedrock AgentCore Runtime microVM environments** via **Terraform**—enabling an absolute zero-cost state on `terraform destroy`.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the current platform architecture and email workflow diagrams.

---

## 📂 Project Directory Structure

```text
langgraph-multi-agent-platform/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # Production Continuous Integration/Deployment workflow
│
├── app/                        # Main application container logic
│   ├── __init__.py
│   ├── agent.py                # Master platform entrypoint & intent router
│   ├── requirements.txt        # Shared environment dependency manifests
│   └── agents/                 # 🧠 Modular agent directory
│       ├── __init__.py
│       └── email_agent/        # Agent Module 1: Automated Email Manager
│           ├── __init__.py
│           ├── graph.py        # LangGraph workflow loops & node logic
│           ├── state.py        # Pydantic core data schemas
│           └── utils/
│               └── send_email.py # Outbound secure SMTP utility wrapper
│
├── infra/                      # Infrastructure as Code (IaC) Staging
│   ├── main.tf                 # Core AWS infrastructure mappings (ECR, IAM, Bedrock)
│   ├── variables.tf            # External input parameters & credentials
│   └── outputs.tf              # Registry targets & environment attributes
│
├── .env.example                # Local configuration documentation template
├── Dockerfile                  # Serverless container compilation script
└── langgraph.json              # Local development engine mapping file
```

---

# 🎨 How to Test Locally Using LangGraph Studio

Follow these simple steps to run your agent locally for free using **Groq** before moving to AWS.

---

### 🧱 Step 1: Set Up Python and Dependencies

1. Install Python on your machine:
   ```bash
   brew install python
   ```
2. Open your terminal and go to your project folder:
   ```bash
   cd langgraph-multi-agent-platform
   ```
3. Create a local virtual environment:
   ```bash
   python3 -m venv .venv
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
5. Install your project packages:
   ```bash
   pip install -r app/requirements.txt
   ```
6. Install the LangGraph developer tool:
   ```bash
   pip install -U "langgraph-cli[inmem]"
   ```

---

### 🔐 Step 2: Set Up Your Secrets File

1. Copy the example configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open the new `.env` file and add your real keys, setting `ENV_TARGET` to `"local"`:
   ```text
   ENV_TARGET="local"
   GROQ_API_KEY="gsk_your_actual_free_groq_key_here"
   
   SENDER_EMAIL="your-email@gmail.com"
   GMAIL_APP_PASSWORD="your-16-digit-gmail-app-password"
   SMTP_SERVER="://gmail.com"
   SMTP_PORT="587"
   ```

---

### 🏃‍♂️ Step 3: Start the Local Server

1. Go to [LangSmith](https://smith.langchain.com/) in your browser and sign up for a free account.
2. Go back to your terminal and start the server:
   ```bash
   langgraph dev
   ```
3. You will see this exact successful output in your terminal:
   ```text
   Welcome to

   ╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
   ║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
   ╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

   - 🚀 API: http://127.0.0.1:2024
   - 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
   - 📚 API Docs: http://127.0.0.1:2024/docs
   ```
4. Click the **`Studio UI`** link directly from your terminal logs (`https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`) to open the visual dashboard in your browser.

---

### 🔬 Step 4: Run and Test Your Agent

1. On the left side of the screen, expand the **`Question`** input field.
2. Type your test message inside it, for example:
   ```text
   Send a leave request to my manager Rahul Kumar from Oct 20 to Oct 25 2026. His email is abc@gmail.com
   ```
3. Click the blue **`Submit`** button at the bottom of the left panel to start running.
4. Watch the visual graph turn green and automatically pause at the pink **`review_node`**.
5. Look at the right side of the screen to see the generated email draft.
6. **To update the draft:** Type your feedback in the right-side box (e.g., *"Make it formal"*) and click submit to re-draft.
7. **To send the email:** Type **`yes`** in the right-side box and click submit to fire the real email via Gmail SMTP.

---

### 🧽 Step 5: How to Start a Fresh Test Run

1. If you hit the feedback limit cap or want to start a completely fresh test, press **`Ctrl + C`** in your terminal to stop the server.
2. Run **`langgraph dev`** again to restart the server with a clean state slate.
3. Refresh your browser page to reset your variables and start over cleanly.




---

# Additional Information

## 🛠️ 1. Step-by-Step Initial Machine Setup

If cloning this repository onto a fresh laptop or reconstructing the space from scratch, execute these configuration phases in chronological order:

### Phase A: Setup the Python Virtual Isolation Layer
1. Navigate to the root directory of the workspace platform:
   ```bash
   cd langgraph-multi-agent-platform
   ```
2. Instantiate a safe, isolated local Python virtual environment to prevent system conflicts:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual container environment wrapper:
   ```bash
   source .venv/bin/activate
   ```
   *(Your terminal prompt will now show `(.venv)` at the beginning of the line).*

### Phase B: Install Required Packages
4. Upgrade your local package installer utility:
   ```bash
   pip install --upgrade pip
   ```
5. Install the official local development engine CLI with embedded tracking frameworks:
   ```bash
   pip install -U "langgraph-cli[inmem]"
   ```
6. Sync and install all core multi-agent runtime application dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

---

## 🎨 2. Local Verification (LangGraph Studio Testing)

Test and debug your graph execution paths locally without provisioning or spending money on cloud resources.

1. Create your local credentials block by creating a copy of the example file:
   ```bash
   cp .env.example .env
   ```
2. Open the newly generated `.env` file and insert your active developer tokens (`GMAIL_APP_PASSWORD`, `SENDER_EMAIL`, etc.).
3. Ensure your local machine has authorized access to call the underlying Amazon Bedrock models:
   ```bash
   aws configure
   ```
4. Fire up the local development visualization engine from the workspace root:
   ```bash
   langgraph dev
   ```
5. **Open the Studio Web UI link** printed in the terminal logs (`https://langchain.com...`) within your browser. 
6. Type a prompt like *"Send an email to user@test.com"* to step through nodes, trigger interrupts, verify revisions, and watch the logic loops run live.

---

## 🏗️ 3. AWS Cloud Infrastructure Deployment (Terraform)

When your local tests pass and you are ready to stage the system onto your live paid AWS environment, execute the manual baseline mapping:

### Phase A: Build Cloud Resources
1. Navigate into the infrastructure configuration staging directory:
   ```bash
   cd infra
   ```
2. Initialize Terraform to download the required AWS cloud infrastructure providers:
   ```bash
   terraform init
   ```
3. Verify changes before executing the construction pipeline:
   ```bash
   terraform plan
   ```
4. Build the baseline architecture (this reads settings securely from your local hidden `terraform.tfvars` file):
   ```bash
   terraform apply -auto-approve
   ```
   *(Note down the printed terminal outputs block once this concludes, highlighting your unique `ecr_repository_url` and `agent_runtime_id`).*

### Phase B: Package and Push the Platform Image
5. Securely authenticate your local machine's Docker daemon into your cloud container registry:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   ```
6. Fall back to the repository workspace root directory context:
   ```bash
   cd ..
   ```
7. Compile your Python application layer into an enterprise container image:
   ```bash
   docker build -t langgraph-multi-agent-platform:latest .
   ```
8. Tag and route your local image build target straight to your remote AWS registry:
   ```bash
   docker tag langgraph-multi-agent-platform:latest <YOUR_AWS_ACCOUNT_ID>://
   ```
9. Upload your built container artifact securely to Amazon ECR:
   ```bash
   docker push <YOUR_AWS_ACCOUNT_ID>://
   ```

### Phase C: Execute the Runtime Registration
10. Trigger a deployment synchronization pass to register your uploaded container image directly into the active serverless Bedrock AgentCore compute pool:
    ```bash
    aws bedrock-agentcore-control update-agent-runtime \
      --agent-runtime-id "<YOUR_AGENT_RUNTIME_ID_FROM_TERRAFORM>" \
      --role-arn "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/langgraph-agentcore-platform-role" \
      --agent-resource-role-arn "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/langgraph-agentcore-platform-role" \
      --agent-runtime-artifact "{\"containerConfiguration\": {\"containerUri\": \"<YOUR_ECR_REPOSITORY_URL_FROM_TERRAFORM>:latest\"}}" \
      --region us-east-1
    ```

---

## 🤖 4. Automated CI/CD (GitHub Actions Integration)

This repository includes a pre-configured continuous integration pipeline inside `.github/workflows/deploy.yml`. To activate seamless automated deployments whenever you push code changes to GitHub:

1. Push your repository code structure up to a public or private GitHub repository.
2. Navigate to your repository dashboard page on GitHub and open **Settings -> Secrets and variables -> Actions**.
3. Create the following required encrypted **Repository Secrets**:
   * `AWS_ACCESS_KEY_ID`: Your IAM programmatic deployer key.
   * `AWS_SECRET_ACCESS_KEY`: Your IAM programmatic deployer password.
   * `AWS_ACCOUNT_ID`: Your 12-digit AWS user account identification string.
   * `SENDER_EMAIL`: The outbound Gmail SMTP sender identifier.
   * `GMAIL_APP_PASSWORD`: The 16-digit generation passkey unlocking SMTP relay.
   * `SMTP_SERVER`: `://gmail.com`
   * `SMTP_PORT`: `587`
4. Now, whenever you push an update to your Python graph logic files or add a new agent module to the `main` branch, the pipeline will automatically rebuild the container, tag it with an immutable Git commit hash, and perform a rolling zero-downtime hot-swap update on AWS!

---

## 🧼 5. The Total Cost-Control Kill Switch (Saving Money)

Because your entire application architecture runs on top of completely serverless resources, you only pay for active execution traffic and basic low-cost image layer persistence. 

However, if you are steping away from development for a few weeks and want absolute peace of mind that **no background charges can accrue on your paid AWS account**, navigate back into your infrastructure tracking directory and run:

```bash
cd infra
terraform destroy -auto-approve
```

Because `force_destroy = true` is hardcoded directly inside your ECR module block, Terraform will cleanly override protection barriers, wipe out your uploaded Docker images, erase your IAM rules, and dismantle your serverless Bedrock runtime environments in seconds—dropping your platform asset footprint billing status straight back to **zero dollars**.
