"""
Contains service endpoints.
"""

import logging
from fastapi import Request, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


from insights_content_template_renderer.utils import render_reports

app = FastAPI()
log = logging.getLogger(__name__)


@app.on_event("startup")
async def expose_metrics():
    """Expose the prometheus metrics in the /metrics endpoint."""
    log.info("Metrics available at /metrics")
    Instrumentator().instrument(app).expose(app)


@app.post("/rendered_reports")
@app.post("/v1/rendered_reports")
async def rendered_reports(request: Request):
    """
    Endpoint for rendering reports based on DoT.js content templates and report details.

    :param request: request containing JSON body with required data
    :return: JSON with rendered reports
    """
    log.info("Received request for /rendered_reports")
    data = await request.json()
    return render_reports(data)
