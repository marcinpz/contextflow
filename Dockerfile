FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/

# Expose port if needed (MCP server)
EXPOSE 8000

# Run the MCP server
CMD ["uv", "run", "python", "-m", "src.mcp.server"]