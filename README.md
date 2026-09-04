# TechNova Office Assistant

Agentic AI Enterprise Employee Assistant built as part of the AI Agentic Training Capstone Project.

## Fictional Company

TechNova Pvt. Ltd.

## Project Objective

The assistant understands employee requests and determines whether the request requires:

- Company policy information
- Employee-specific information
- Tool/database access
- Multiple information sources

## Knowledge Base

The project contains 11 fictional company policy documents covering:

- Employee Handbook
- Leave Policy
- Travel Policy
- Reimbursement Policy
- Work From Home Policy
- IT Policy
- Security Policy
- Onboarding Guide
- Office Guidelines
- Expense Policy
- Benefits Guide

## Structured Data

The project contains sample data for:

- Employees
- Leave balances
- Expense records
- IT assets
- Office locations

## Architecture

User
→ Intent Agent
→ RAG / Tools
→ LLM
→ Grounded Response

## RAG

Policy documents are converted into embeddings and stored in a vector database.

The retrieval layer returns:

- Relevant text
- Source document
- Page number

## Status

Initial knowledge base and structured datasets created.
