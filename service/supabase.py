# Supabase
from supabase import create_client, Client
url: str = "https://ymotfwhygudyyjbzkgrb.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inltb3Rmd2h5Z3VkeXlqYnprZ3JiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI1NzEyMjgsImV4cCI6MjAyODE0NzIyOH0.AasZjsrYh9LLyiY-nWJBn_s2oCfkLFTZOdN23TDt4W0"

supabase: Client = create_client(url, key)
