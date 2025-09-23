import os
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource(attributes={
    "service.name": "tiny-api-service"
})
otlp_exporter = OTLPSpanExporter()
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

app = FastAPI()

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


@app.get("/greet")
async def greet(name: str = "World"):
    welcome_prefix = os.getenv("WELCOME_PREFIX", "Hello")
    return {"greeting": f"{welcome_prefix}, {name}!"}