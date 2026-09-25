# IBMPoc

IBM watsonx.ai + IBM Bob + watsonx Orchestrate — AI-assisted SDLC proof of concept.

## Overview
This repository is the code output layer of the AI SDLC pipeline:

| Stage | Tool | Output |
|---|---|---|
| 1. Story creation | watsonx Orchestrate nalyst_story_crafter | Jira ticket (SCRUM project) |
| 2. Ticket triage  | watsonx Orchestrate cognitive_ticket_triage | Assigned tickets |
| 3. BRD generation | IBM Bob /brd-generator | generated/docs/BRD_<KEY>.md |
| 4. FSD generation | IBM Bob /fsd-generator | generated/docs/FSD_<KEY>.md |
| 5. Code scaffold  | watsonx Orchestrate github_dev_agent | Feature branch + draft PR |

## Structure
```
src/          # Backend Python Flask routes
templates/    # HTML frontend templates
tests/        # pytest test files
generated/    # AI-generated BRD / FSD documents
```

## Jira
https://firstcode-team-oidvioym.atlassian.net/browse/SCRUM

## Stack
- IBM watsonx.ai (Llama 3.3 70B)
- IBM Bob (VS Code AI assistant)
- watsonx Orchestrate
- Jira Cloud
- GitHub