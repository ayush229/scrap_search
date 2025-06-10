import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess
import os
import json
import uuid
import asyncio

from utils.vector_store import VectorStore
from utils.llm_interaction import LLMInteraction

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
vector_store = VectorStore()
llm_interaction = LLMInteraction(api_key=os.getenv("GROQ_API_KEY"))

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

class ScrapAndStoreRequest(BaseModel):
    urls: str

class QuerySearchRequest(BaseModel):
    user_query: str
    agent_key: str

@app.post("/scrap_and_store", summary="Scrap content from URLs, vectorize, and store")
async def scrap_and_store(request: ScrapAndStoreRequest):
    """
    Scraps content from the provided URLs (comma-separated),
    converts it into vectors, and stores it locally.
    Returns the scrapped content and an alphanumeric agent key.
    """
    urls = [url.strip() for url in request.urls.split(',') if url.strip()]
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs provided.")

    scraped_data_list = []
    agent_key = str(uuid.uuid4()) # Generate a unique agent key

    for url in urls:
        try:
            # Run Scrapy spider as a subprocess
            # The output will be a JSON array of scraped items
            process = await asyncio.create_subprocess_exec(
                "scrapy", "crawl", "generic_spider",
                "-a", f"start_url={url}",
                "-o", "-", # Output to stdout
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                # MODIFIED: Print and include stderr in the HTTPException detail
                error_message = stderr.decode(errors='ignore').strip() # Decode with error handling
                print(f"Scrapy process returned non-zero exit code for {url}. Stderr: {error_message}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Scraping failed for {url}. Error: {error_message if error_message else 'Unknown Scrapy error (no stderr output). See container logs for more details.'}"
                )

            # Decode and parse the JSON output from Scrapy
            scraped_items = json.loads(stdout.decode())
            if scraped_items:
                # Assuming each item has a 'content' field
                full_content_for_url = " ".join([item.get('content', '') for item in scraped_items])
                scraped_data_list.append({
                    "url": url,
                    "content": full_content_for_url,
                    "beautified_content": scraped_items # Provide the raw scraped items for beautified format
                })
                # Store the vectorized content
                vector_store.store_data(agent_key, url, full_content_for_url)
            else:
                scraped_data_list.append({
                    "url": url,
                    "content": "No content scraped.",
                    "beautified_content": []
                })

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error during scraping for {url}: {str(e)}")

    return {
        "message": "Scraping and storage successful.",
        "agent_key": agent_key,
        "scrapped_content": scraped_data_list
    }

@app.post("/query_search", summary="Query the stored content using AI")
async def query_search(request: QuerySearchRequest):
    """
    Takes a user query, matches it with stored vectorized data for a given agent key,
    and provides an AI-generated response strictly from the matched content.
    """
    user_query = request.user_query
    agent_key = request.agent_key

    # Retrieve and match content for the given agent key
    matched_content = vector_store.retrieve_matched_content(agent_key, user_query)

    if not matched_content:
        return {
            "response": "Fallback: The asked query does not match or is not found in the stored data for this agent key.",
            "source": "None"
        }

    # Pass matched content and query to LLM
    response_from_llm = llm_interaction.get_ai_response(user_query, matched_content)

    return {
        "response": response_from_llm,
        "source_content_used": matched_content # For debugging/verification
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) # Changed port to 8080
