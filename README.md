Project: Netflix Serverless Data Engineering Pipeline

Objective:
Build a fully serverless ELT pipeline to ingest, validate, transform, and analyze Netflix dataset from GitHub using AWS services (Lambda, S3, Glue, Athena) following best practices of a layered data lake.

Architecture Overview
GitHub CSV
    ↓ (Lambda 1)
Amazon S3 Raw Layer
    ↓ (Lambda 2 - Validation & Orchestration)
Amazon S3 Processed Layer
    ↓ (AWS Glue PySpark Job)
Amazon S3 Curated Layer (Parquet)
    ↓ (Glue Crawler)
Amazon Athena (Query & Analytics)


Layers:

Raw: Immutable CSV directly from GitHub

Processed: Validated CSV, ready for transformation

Curated: Cleaned, transformed Parquet dataset optimized for analytics

Technical Workflow

Data Ingestion

AWS Lambda pulls CSV from GitHub raw URL

Validates that content is CSV (avoids HTML downloads)

Stores in S3 Raw Layer

Data Validation & Layer Transition

Second Lambda triggers on S3 PUT event

Validates CSV structure and file size

Moves data to Processed Layer in S3

Data Transformation

AWS Glue PySpark Job reads CSV from processed layer

Cleans columns, parses date_added, splits listed_in

Deduplicates by show_id

Writes Parquet files to curated layer

Data Catalog & Analytics

Glue Crawler scans curated layer

Creates Athena table: curated

Enables SQL-based analytics for reporting and insights
