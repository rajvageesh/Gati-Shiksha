from waitress import serve
from app import app
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    print("Starting Waitress Production Server on http://0.0.0.0:8000...")
    
    # Waitress configuration for production DoS defense:
    # - threads: Limits concurrent processing (prevents CPU exhaustion)
    # - connection_limit: Prevents connection flooding
    # - clear_untrusted_proxy_headers: Security precaution
    # - channel_timeout: Kills idle connections (Slowloris defense)
    serve(
        app,
        host='0.0.0.0',
        port=8000,
        threads=4,
        connection_limit=1000,
        channel_timeout=30,
        clear_untrusted_proxy_headers=True
    )
