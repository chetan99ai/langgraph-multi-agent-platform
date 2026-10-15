# Architecture

This page diagrams the architecture implemented by the repository: local LangGraph Studio development, the AgentCore runtime path, the email workflow, and the GitHub Actions deployment path.

## Platform overview

```mermaid
flowchart LR
    subgraph Dev["Local development"]
        Studio["LangGraph Studio"]
        LocalGraph["email_graph<br/>from langgraph.json"]
        LocalModel["Groq<br/>openai/gpt-oss-20b"]
        Studio --> LocalGraph
    end

    subgraph Delivery["Build and delivery"]
        Push["Push to main"]
        Actions["GitHub Actions<br/>deploy.yml"]
        TF["Terraform<br/>infra/"]
        Build["Docker build"]
        ECR["Amazon ECR<br/>container image"]
        Update["Update AgentCore runtime<br/>with commit-tagged image"]
        Push --> Actions
        Actions --> TF
        Actions --> Build --> ECR --> Update
    end

    subgraph AWS["AWS runtime"]
        Caller["API client"]
        Endpoint["AgentCore runtime endpoint"]
        Runtime["Bedrock AgentCore Runtime<br/>container: app/agent.py"]
        Router["Intent and session router<br/>orchestrate_platform_agents"]
        Graph["Email LangGraph<br/>email_graph"]
        Role["AgentCore execution role<br/>ECR image pull + Bedrock invoke"]
        Bedrock["Amazon Bedrock<br/>amazon.nova-pro-v1:0"]
        SMTP["SMTP server"]

        Caller --> Endpoint --> Runtime --> Router --> Graph
        Runtime -. assumes .-> Role
        Graph -. "ENV_TARGET=aws" .-> Bedrock
        Graph --> SMTP
    end

    LocalGraph --> LocalModel
    TF --> ECR
    TF --> Role
    TF --> Endpoint
    Update --> Runtime

    classDef user fill:#e8f1ff,stroke:#3973ac,color:#15283f
    classDef app fill:#f0eaff,stroke:#7952a3,color:#271a3c
    classDef aws fill:#fff1dc,stroke:#d18416,color:#3b2910
    classDef delivery fill:#e6f5ec,stroke:#398252,color:#193523
    class Studio,Caller user
    class LocalGraph,Router,Graph,Runtime app
    class Endpoint,Role,ECR,Bedrock,SMTP aws
    class Push,Actions,TF,Build,Update delivery
```

## Email workflow

The platform router sends new email-related requests to the email graph. If a session is paused for review, the next input resumes that graph; approval sends the email, while feedback requests another draft.

```mermaid
flowchart TD
    Start([Request]) --> Extract["Retriever<br/>extract recipient and reason"]
    Extract --> Draft["Draft email<br/>generate or revise subject and body"]
    Draft --> Review["Human review interrupt<br/>show draft and wait for input"]
    Review --> Decision{"Approval or feedback?"}
    Decision -- "yes" --> Send["Send via SMTP"]
    Send --> Done([Complete])
    Decision -- "feedback" --> Limit{"More than 2 feedback rounds?"}
    Limit -- "no" --> Draft
    Limit -- "yes" --> Cancel["Return not-sent response"]
    Cancel --> Done
```

The graph shares `EmailState` between nodes. Structured output schemas (`UserDetails` and `DraftEmail`) define the LLM extraction and draft results. Requests that do not match the email intent currently receive the router's fallback response.

## Configuration notes

- The LLM connector is selected by `ENV_TARGET`: `aws` uses Amazon Bedrock; any other value (including the default `local`) uses Groq. Terraform currently does not set `ENV_TARGET`, so the deployed container defaults to the Groq path unless it is configured separately.
- The GitHub Actions workflow builds a Docker image, but the checked-in `Dockerfile` currently contains only a comment. The image build step therefore needs a real Dockerfile before this deployment path can run successfully.
- The graph is compiled without an explicit checkpointer, while the AgentCore entrypoint queries graph state to resume interrupted sessions. Verify the runtime's thread-state integration before relying on approval/resume across requests.
- Local Studio loads `email_graph` directly from `langgraph.json`; the AWS AgentCore entrypoint and intent router are in `app/agent.py`.
