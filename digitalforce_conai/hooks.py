# -*- coding: utf-8 -*-
import logging
import requests

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    try:
        requests.post(
            "https://license.digitalforce.it/api/v1/ping",
            json={
                "event": "install",
                "module": "digitalforce_conai",
                "database_uuid": env["ir.config_parameter"].sudo().get_param("database.uuid"),
                "company_name": env.company.name,
            },
            timeout=3,
        )
    except requests.RequestException:
        _logger.info("CONAI install ping failed (non-critical, no functional impact).")
