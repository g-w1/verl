from datetime import datetime
import json
import os
import uuid
import dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions

dotenv.load_dotenv(override=True, dotenv_path="../../.env")

def create_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key, options=ClientOptions(postgrest_client_timeout=5000, storage_client_timeout=5000))
    return supabase
def add_experiment_to_supabase(client: Client, experiment_uuid: str):
    try:
        client.table("experiments").insert({
            "id": experiment_uuid,
        }).execute()
    except Exception as e:
        print('=' * 100, "Error adding experiment to supabase", e, '=' * 100)
        raise e

def add_step(client: Client, experiment_uuid: str, step_results: dict, global_step: int, is_train_step: bool):
    table_name = "experiment_train_step" if is_train_step else "experiment_val_step"
    jsonb_metrics = json.dumps(step_results)
    try:
        client.table(table_name).insert({
            "experiment_id": experiment_uuid,
            "step_results": jsonb_metrics,
            "global_step": global_step
        }).execute()
    except Exception as e:
        print(step_results)
        print('=' * 100, "Error adding step to supabase", e, '=' * 100)
        raise e
